from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import RPi.GPIO as GPIO

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import logging
import json
import random

import time
import datetime
import threading


AllowedActions = ['both', 'publish', 'subscribe']

# specify the period as integer second
sensorReadPeriod = 1  # 1 sec
awsSendPeriod = 5     # 5 sec
awsListenPeriod = 5   # 5 sec

autoMode = True    # 0: auto mode; 1: manual mode
waterFlag = False
rotateFlag = False
iotConnected = False
desired_hum = 0

para = dict()

def on_connect(client, userdata, flags, rc):
    if rc == 0:

        print("Connected to IoT")

        global iotConnected  # Use global variable
        iotConnected = True  # Signal connection

    else:
        print("Connection failed")


def on_message(client, userdata, message):
    print("---------------------------\n"
          "Received a new message from IoT \n ")
          
    json_string = message.payload.decode("utf-8") 
    json_string = json_string.replace("u'", "\"").replace("'", "\"")
    data = json.loads(json_string)
    try:
        if data['cmd'] == 'control':
            global waterFlag, rotateFlag
            if data['val'] == 'water_start':
                GPIO.output(para['pinPump'], 1)
                waterFlag = True
                time.sleep(1)
                GPIO.output(para['pinPump'], 0)
                waterFlag = False

                print('Watering the plant')
            elif data['val'] == 'water_stop':
                GPIO.output(para['pinPump'], 0)
                waterFlag = False

                print('Stop watering')
            elif data['val'] == 'rotate_start':
                GPIO.output(para['pinDisc'], 1)
                rotateFlag = True

                print('Rotating the disc')
            elif data['val'] == 'rotate_stop':
                GPIO.output(para['pinDisc'], 0)
                rotateFlag = False

                print('Stop rotating')
            else:
                print("Unknown control value")
        elif data['cmd'] == 'mode_switch':
            global autoMode
            if data['val'] == 'auto':
                autoMode = True
                print('Change mode to auto')
            elif data['val'] == 'manual':
                autoMode = False
                print('Change mode to manual')
        elif data['cmd'] == 'humidity_control':
            #global desired_hum
            #desired_hum = str(data['val'])
            print('Set desired humidity to ')
            print(data['val'])
            #print('Set desired humidity to {:.0f}'.format(desired_hum))
    except:
        print('Unknown command')
    print("---------------------------")


def sensorConfig():
    """
    config sensors
    """
    # GPIO.cleanup()
    i2c = busio.I2C(board.SCL, board.SDA)

    global para
    para['ads'] = ADS.ADS1115(i2c)

    para['pinPump'] = 21
    para['pinDisc'] = 26
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(para['pinPump'], GPIO.OUT)
    GPIO.setup(para['pinDisc'], GPIO.OUT)
    GPIO.output(para['pinPump'], 0)
    GPIO.output(para['pinDisc'], 0)



def sensorReading(para):
    """
    read data sensors
    """
    reading = {}
    reading['mois'] = AnalogIn(para['ads'], ADS.P1).voltage
    reading['uv'] = AnalogIn(para['ads'], ADS.P2).voltage

    # if readMoisSens > 2.4:
    #     GPIO.output(para['pinMoisSens'], 1)
    #     print('Too dry, water the flower \nCurrent reading: {:.2f}'
    #           .format(readMoisSens))
    # else:
    #     GPIO.output(para['pinMoisSens'], 0)
    #     print('the flow is fine now \nCurrent reading: {:.2f}'
    #           .format(readMoisSens))

    return reading

def awsConfig():
    """
    connect to AWS
    """
    host = "a1x0fiabery709-ats.iot.us-east-2.amazonaws.com"
    rootCAPath = "cert/root-CA.pem"
    certificatePath = "cert/4ad4027780-certificate.pem.crt"
    privateKeyPath = "cert/4ad4027780-private.pem.key"
    port = 8883
    clientId = "TEST_COMM"
    upstream_topic = "$aws/things/cse521/shadow/message_to_iot"
    downstream_topic = "$aws/things/cse521/shadow/message_to_pi"

    # myAWSIoTMQTTClient = None
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
    myAWSIoTMQTTClient.configureDrainingFrequency(2)
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(awsSendPeriod)  # 5 sec

    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.on_connect = on_connect
    myAWSIoTMQTTClient.on_message = on_message

    myAWSIoTMQTTClient.connect()
    myAWSIoTMQTTClient.subscribe(downstream_topic, 1, on_message)


    return myAWSIoTMQTTClient, upstream_topic

def awsSending(client, topic, data):
    """
    send data to AWS
    """
    message = {}
    message["time"] = str(datetime.datetime.now())

    info = {}

    for key, value in data.items():
        message[key] = value
        
    # message["message"] = data
    messageJson = json.dumps(message)
    client.publish(topic, messageJson, 1)


def collectData(para, moisDataList, UVDataList, data):
    moisreading = round(-42.9 * sensorReading(para)['mois'] + 156.6)
    moisDataList.append(moisreading)
    uvreading = round(sensorReading(para)['uv'] * 10, 1)
    UVDataList.append(uvreading)
    print('Moisure reading: {:.0f}%, UV reading: {:.1f} index'
          .format(moisreading, uvreading))
    # print('reading done')
    data['Humidity'] = moisDataList
    data['UV'] = UVDataList


def sendData(awsClient, toIotTopic, data, moisDataList, UVDataList):
    # get averaged readings for each sensor
    for key, value in data.items():
        data[key] = round(sum(value) / len(value), 1)

    # publish message to iot
    awsSending(awsClient, toIotTopic, data)
    print('Sent to AWS')

    # clean up reading data
    data = {}
    moisDataList = []
    UVDataList = []



def main():
    sensorConfig()
    awsClient, toIotTopic = awsConfig()

    data = {}
    moisDataList = []
    UVDataList = []
    j = 0
    
    for i in range(1,300):
        if not i % awsSendPeriod:

            # get averaged readings for each sensor
            for key, value in data.items():
                data[key] = round(sum(value)/len(value), 1)

            # publish message to iot
            awsSending(awsClient, toIotTopic, data)
            print('Sent to AWS')

            j = 0
            data = {}
            moisDataList = []
            UVDataList = []
        elif not i % sensorReadPeriod:
            moisreading = round(-42.9*sensorReading(para)['mois']+156.6)
            moisDataList.append(moisreading)
            uvreading = round(sensorReading(para)['uv']*10, 1)
            UVDataList.append(uvreading)
            print('Moisure reading: {:.0f}%, UV reading: {:.1f} index'
                 .format(moisreading, uvreading))
            # print('reading done')
            data['Humidity'] = moisDataList
            data['UV'] = UVDataList
            j += 1
        else:
            print("Nothing to do now")

        time.sleep(1)

    GPIO.cleanup()




if __name__ == "__main__":
    main()

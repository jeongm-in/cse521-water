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

mode = 0    # 0: auto mode; 1: manual mode
Connected = False

para = dict()


def on_connect(client, userdata, flags, rc):
    if rc == 0:

        print("Connected to IoT")

        global Connected  # Use global variable
        Connected = True  # Signal connection

    else:
        print("Connection failed")


def on_message(client, userdata, message):
    print("---------------------------\n"
          "Received a new message from IoT \n ")
          
    json_string = message.payload.decode("utf-8") 
    json_string = json_string.replace("u'", "\"").replace("'", "\"")
    data = json.loads(json_string)
    #data = message.payload
    #print(type(message.payload))
    #print(type(str(message.payload)))
    try:
        if data['mode'] == 'control':
            if data['val'] == 'water':
                GPIO.output(para['pinPump'], 1)
                print('Watering by the request of IoT')
            elif data['val'] == 'stop':
                GPIO.output(para['pinPump'], 0)
                print('Stop watering')
        elif data['mode'] == 'mode_switch':
            global mode
            if data['val'] == 'auto':
                mode = 0
                print('Change mode to auto')
            else:
                mode = 1
                print('Change mode to manual')
    except:
        print('unrocognized command')
    print("---------------------------")

def sensorConfig():
    """
    config sensors
    """
    GPIO.cleanup()
    i2c = busio.I2C(board.SCL, board.SDA)

    global para
    para['ads'] = ADS.ADS1115(i2c)

    para['pinPump'] = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(para['pinPump'], GPIO.OUT)
    GPIO.output(para['pinPump'], 0)



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
    # myAWSIoTMQTTClient.loop_start()  # start the loop
    #while not Connected:  # Wait for connection
    #    time.sleep(0.1)
    # myAWSIoTMQTTClient.subscribe(downstream_topic)
    myAWSIoTMQTTClient.subscribe(downstream_topic, 1, on_message)


    return myAWSIoTMQTTClient, upstream_topic

def awsSending(client, topic, data):
    """
    send data to AWS
    """
    message = {}
    message["time"] = str(datetime.datetime.now())

    info = {}

    for key in data.keys():
        message['mode'] = key
        message['val'] = data[key]
        
    # message["message"] = data
    messageJson = json.dumps(message)
    client.publish(topic, messageJson, 1)


def main():
    sensorConfig()
    awsClient, toIotTopic = awsConfig()
    
    j = 0
    data = {}
    moisDataList = []
    UVDataList = []
    for i in range(1,100):
        if not i % awsSendPeriod:

            # get averaged readings for each sensor
            for key in data:
                data[key] = sum(data[key])/len(data[key])

            # publish message to iot
            awsSending(awsClient, toIotTopic, data)
            print('Sent to AWS')
            
            j = 0
            data = {}
            moisDataList = []
            UVDataList = []
        elif not i % sensorReadPeriod:
            moisDataList.append(sensorReading(para)['mois'])
            UVDataList.append(sensorReading(para)['uv'])
            print('Moisure reading: {:.2f}, UV reading: {:.2f}'
                 .format(sensorReading(para)['mois'],sensorReading(para)['uv']))
            # print('reading done')
            data['moisture'] = moisDataList
            data['UV'] = UVDataList
            j += 1
        else:
            print("Nothing to do now")
            
        time.sleep(1)

    GPIO.cleanup()


if __name__ == "__main__":
    main()

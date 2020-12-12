from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import RPi.GPIO as GPIO



import logging
import json
import random

import time
import datetime

from helperFun import *

AllowedActions = ['both', 'publish', 'subscribe']

# specify the period as integer second
sensorReadPeriod = 1  # 1 sec
awsSendPeriod = 5     # 5 sec
awsListenPeriod = 5   # 5 sec


def sensorReading(para):
    """
    read data sensors
    """
    reading = {}
    reading['mois'] = AnalogIn(para['ads'], ADS.P1).voltage
    reading['uv'] = AnalogIn(para['ads'], ADS.P2).voltage

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
    print(data)


def sendData(awsClient, toIotTopic, data, moisDataList, UVDataList):
    # get averaged readings for each sensor
    for key, value in data.items():
        data[key] = round(sum(value) / len(value), 1)

    # publish message to iot
    awsSending(awsClient, toIotTopic, data)
    print('Sent to AWS')

    # clean up reading data
    data = {}
    moisDataList.clear()
    UVDataList.clear()
    print("cleaned")


def main():
    sensorConfig()
    awsClient, toIotTopic = awsConfig()

    data = {}
    moisDataList = []
    UVDataList = []

    
    tCollectData = RepeatedTimer(sensorReadPeriod, collectData, para, moisDataList, UVDataList, data)
    tSendData = RepeatedTimer(awsSendPeriod, sendData, awsClient, toIotTopic, data, moisDataList, UVDataList)
    
    tCollectData.joinEnable(True)

    waterFlag_old = waterFlag
    rotateFlag_old = rotateFlag

    while True:
        humidity_control = 50


        while autoMode:     # in auto mode
            autoBehave(moisDataList, UVDataList, humidity_control, waterFlag_old, rotateFlag_old)
            # , waterFlag_old, rotateFlag_old

            time.sleep(.5)
            print("waterFlag_old: {}".format(waterFlag_old))
        while not autoMode: # in manual mode

            time.sleep(1)



if __name__ == "__main__":
    main()

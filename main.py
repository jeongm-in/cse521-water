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

def customCallback(client, userdata, message):
    print("Received a new message")
    print(message.payload)
    print("from topic")
    print(message.topic)
    print("------\n\n")


def sensorConfig():
    """
    config sensors
    """
    para = dict()

    GPIO.cleanup()
    i2c = busio.I2C(board.SCL, board.SDA)
    para['ads'] = ADS.ADS1115(i2c)

    para['pinMoisSens'] = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(para['pinMoisSens'], GPIO.OUT)

    return para


def sensorReading(para):
    """
    read data sensors
    """
    readMoisSens = AnalogIn(para['ads'], ADS.P1).voltage

    # if readMoisSens > 2.4:
    #     GPIO.output(para['pinMoisSens'], 1)
    #     print('Too dry, water the flower \nCurrent reading: {:.2f}'
    #           .format(readMoisSens))
    # else:
    #     GPIO.output(para['pinMoisSens'], 0)
    #     print('the flow is fine now \nCurrent reading: {:.2f}'
    #           .format(readMoisSens))

    return readMoisSens

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
    topic = "$aws/things/cse521/shadow/sensor_reading"

    myAWSIoTMQTTClient = None
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
    myAWSIoTMQTTClient.configureDrainingFrequency(2)
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(awsSendPeriod)  # 5 sec

    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()

    return myAWSIoTMQTTClient, topic

def awsSending(client, topic, data):
    """
    send data to AWS
    """
    message = {}
    message["message"] = "hello"

    state = {}
    state['reported'] = {}
    state['reported']['time'] = str(datetime.datetime.now())

    for key in data.keys():
        state['reported'][key] = data[key]
        
    message["state"] = state
    messageJson = json.dumps(message)
    client.publish(topic, messageJson, 1)


def main():
    para = sensorConfig()
    awsClient, topic = awsConfig()
    
    j = 0
    data = {}
    moisDataList = []
    for i in range(1,100):
        if not i % awsSendPeriod:
            awsSending(awsClient, topic, data)
            print('sending done')
            
            j = 0
            data = {}
            moisDataList = []
        elif not i % sensorReadPeriod:
            moisDataList.append(sensorReading(para))
            print('reading done')
            data['moisture'] = moisDataList
            j += 1
        else:
            print("Nothing to do now")

        time.sleep(1)

    GPIO.cleanup()


if __name__ == "__main__":
    main()

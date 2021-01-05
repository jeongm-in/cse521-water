# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import sys


# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a1x0fiabery709-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERT = "/var/script/awsiot/cert.pem.crt"
PATH_TO_KEY = "/var/script/awsiot/private.pem.key"
PATH_TO_ROOT = "/var/script/awsiot/root.pem"
MESSAGE = "Hello World"
TOPIC = "$aws/things/cse521/shadow/message_to_pi"
RANGE = 20
mode = sys.argv[1]
val = sys.argv[2]

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

myAWSIoTMQTTClient.connect()
print('Begin Publish')

message = {"cmd" : mode,"val":val}
myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 1) 
print("Published: '" + json.dumps(message) + "' to the topic: " + "'message_to_pi'")

myAWSIoTMQTTClient.disconnect()
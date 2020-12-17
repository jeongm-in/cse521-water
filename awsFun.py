from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import RPi.GPIO as GPIO

import json
import time
import datetime

import sensorFun as sf
import helperFun as hf

awsSendPeriod = 5     # 5 sec
iotConnected = False
AllowedActions = ['both', 'publish', 'subscribe']



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


"""
when receive message from IoT
"""
def on_message(client, userdata, message):
    print("---------------------------\n"
          "Received a new message from IoT \n ")

    json_string = message.payload.decode("utf-8")
    json_string = json_string.replace("u'", "\"").replace("'", "\"")
    data = json.loads(json_string)

    try:
        para = sf.pinMap()
        if data['cmd'] == 'control':
            if hf.autoMode:
                print('Auto mode is ON, switch to manual mode first')
            else:
                if data['val'] == 'water_start':
                    GPIO.output(para['pinPump'], 1)
                    hf.waterFlag = True
                    print('Manual: Watering the plant')

                    time.sleep(1)
                    GPIO.output(para['pinPump'], 0)
                    hf.waterFlag = False
                    print('And stop')

                elif data['val'] == 'water_stop':
                    GPIO.output(para['pinPump'], 0)
                    hf.waterFlag = False

                    print('Manual: Stop watering')
                elif data['val'] == 'rotate_start':
                    # GPIO.output(para['pinDisc'], 1)
                    hf.rotateFlag = True

                    print('Manual: Rotating the disc')
                elif data['val'] == 'rotate_stop':
                    # GPIO.output(para['pinDisc'], 0)
                    hf.rotateFlag = False

                    print('Manual: Stop rotating')
                else:
                    print("Unknown control value")
        elif data['cmd'] == 'mode_switch':
            if data['val'] == 'auto':
                hf.autoMode = True

                print('Change mode to auto')
            elif data['val'] == 'manual':
                hf.autoMode = False

                print('Change mode to manual')
        elif data['cmd'] == 'humidity_control':
            hf.desired_hum = int(data['val'])

            print('Set desired humidity to ')
            print(data['val'])
    except:
        print('Unknown command')
    print("---------------------------")


def on_connect(client, userdata, flags, rc):
    if rc == 0:

        print("Connected to IoT")

        global iotConnected  # Use global variable
        iotConnected = True  # Signal connection

    else:
        print("Connection failed")


def awsSending(client, topic, data):
    """
    send data to AWS
    """
    message = {}
    message["time"] = str(datetime.datetime.now())

    for key, value in data.items():
        message[key] = value

    messageJson = json.dumps(message)
    client.publish(topic, messageJson, 1)
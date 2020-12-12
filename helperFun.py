import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from threading import Timer
import time
import RPi.GPIO as GPIO
import json

autoMode = True  # 0: auto mode; 1: manual mode
waterFlag = False
rotateFlag = False
iotConnected = False
desired_hum = 0

para = dict()


"""
repeat timer class
"""
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def joinEnable(self, val):
        if val:
            self._timer.join()


"""
config sensors
"""
def sensorConfig():

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


"""
when receive message from IoT
"""
def on_message(client, userdata, message):
    print("---------------------------\n"
          "Received a new message from IoT \n ")

    json_string = message.payload.decode("utf-8")
    json_string = json_string.replace("u'", "\"").replace("'", "\"")
    data = json.loads(json_string)
    global autoMode
    try:
        if data['cmd'] == 'control':
            if autoMode:
                print('Auto mode is ON, switch to manual mode first')
            else:
                global waterFlag, rotateFlag
                if data['val'] == 'water_start':
                    GPIO.output(para['pinPump'], 1)
                    waterFlag = True
                    time.sleep(1)
                    GPIO.output(para['pinPump'], 0)
                    waterFlag = False

                    print('Manual: Watering the plant')
                elif data['val'] == 'water_stop':
                    GPIO.output(para['pinPump'], 0)
                    waterFlag = False

                    print('Manual: Stop watering')
                elif data['val'] == 'rotate_start':
                    GPIO.output(para['pinDisc'], 1)
                    rotateFlag = True

                    print('Manual: Rotating the disc')
                elif data['val'] == 'rotate_stop':
                    GPIO.output(para['pinDisc'], 0)
                    rotateFlag = False

                    print('Manual: Stop rotating')
                else:
                    print("Unknown control value")
        elif data['cmd'] == 'mode_switch':
            if data['val'] == 'auto':
                autoMode = True

                print('Change mode to auto')
            elif data['val'] == 'manual':
                autoMode = False

                print('Change mode to manual')
        elif data['cmd'] == 'humidity_control':
            global desired_hum
            desired_hum = data['val']

            print('Set desired humidity to ')
            print(data['val'])
            # print('Set desired humidity to {:.0f}'.format(desired_hum))
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



"""
when set as auto mode
"""
def autoBehave(moisDataList, UVDataList, humidity_control, waterFlag_old, rotateFlag_old):
    try:
        moisAvg = round(sum(moisDataList) / len(moisDataList), 1)
        UVAvg = round(sum(UVDataList) / len(UVDataList), 1)

        if moisAvg < humidity_control:  # if more dry than the preset humidity, open pump
            GPIO.output(para['pinPump'], 1)
            waterFlag = True
        else:  # if not, close pump
            GPIO.output(para['pinPump'], 0)
            waterFlag = False

        if not waterFlag_old and waterFlag:  # if becomes dry
            print("Auto: too dry, water the plant")
        elif waterFlag_old and not waterFlag:
            print("Auto: proper humidity")

        if UVAvg > .5:  # if there is sunlight, rotate disk
            GPIO.output(para['pinDisc'], 1)
            rotateFlag = True
        else:  # if not, stop rotating
            GPIO.output(para['pinDisc'], 0)
            rotateFlag = False

        if not rotateFlag_old and rotateFlag:  # if sunlight becomes available
            print("Auto: Sunlight! Rotating disk")
        elif waterFlag_old and not waterFlag:
            print("Auto: No Sunlight! Stop Rotating")

        waterFlag_old = waterFlag
        rotateFlag_old = rotateFlag

    except:
        print("-")
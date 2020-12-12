from threading import Timer
import time
import RPi.GPIO as GPIO
import json

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
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
            # global desired_hum
            # desired_hum = str(data['val'])
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
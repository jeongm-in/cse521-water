from threading import Timer
import RPi.GPIO as GPIO

import awsFun as af
import sensorFun as sf


autoMode = True  # True: auto mode; False: manual mode
desired_hum = 50
waterFlag = False
rotateFlag = False



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


class DiskRotation(object):
    def __init__(self, pin, *args, **kwargs):
        self.iter = 0
        self.totalIter = 0
        self.halfStep_seq = [
          [1,0,0,0],
          [1,1,0,0],
          [0,1,0,0],
          [0,1,1,0],
          [0,0,1,0],
          [0,0,1,1],
          [0,0,0,1],
          [1,0,0,1]
        ]
        self.pin = pin

    def getIter(self):
        return self.iter

    def updateIter(self):
        self.totalIter = self.totalIter+1
        self.iter = self.totalIter % 8
        if self.totalIter >= 400:
            self.totalIter = 0

            global rotateFlag
            rotateFlag = False

    def rotate(self):
        for num in range(4):
            GPIO.output(self.pin[num], self.halfStep_seq[self.iter][num])

        self.updateIter()


def collectData(para, moisDataList, UVDataList, data):
    moisreading = round(-42.9 * sf.sensorReading(para)['mois'] + 156.6)
    moisDataList.append(moisreading)
    uvreading = round(sf.sensorReading(para)['uv'] * 10, 1)
    UVDataList.append(uvreading)
    print('Moisure reading: {:.0f}%, UV reading: {:.1f} index'
          .format(moisreading, uvreading))

    data['Humidity'] = moisDataList
    data['UV'] = UVDataList
    # print(data)


def sendData(awsClient, toIotTopic, data, moisDataList, UVDataList):
    # get averaged readings for each sensor
    for key, value in data.items():
        data[key] = round(sum(value) / len(value), 1)

    # publish message to iot
    af.awsSending(awsClient, toIotTopic, data)
    print('Sent to AWS')

    # clean up reading data
    data = dict()
    moisDataList.clear()
    UVDataList.clear()


"""
execute at auto mode
"""
def autoBehave(moisDataList, UVDataList, desired_hum, waterFlag_old, rotateFlag_old):

    try:
        moisAvg = round(sum(moisDataList) / len(moisDataList), 1)
        UVAvg = round(sum(UVDataList) / len(UVDataList), 1)

        global waterFlag, rotateFlag
        para = sf.pinMap()

        if moisAvg < desired_hum:  # if more dry than the preset humidity, open pump
            GPIO.output(para['pinPump'], 1)
            waterFlag = True
            print('dry: {.2f}%, {.2f}%'.format(moisAvg, desired_hum))
        else:  # if not, close pump
            GPIO.output(para['pinPump'], 0)
            waterFlag = False
            print('wet')


        if not waterFlag_old and waterFlag:  # if becomes dry
            print("Auto: too dry, START watering")
        elif waterFlag_old and not waterFlag:
            print("Auto: proper humidity, STOP watering")

        if UVAvg > .5:  # if there is sunlight, rotate disk
            # GPIO.output(para['pinDisc'], 1)
            rotateFlag = True
        else:  # if not, stop rotating
            # GPIO.output(para['pinDisc'], 0)
            rotateFlag = False

        if not rotateFlag_old and rotateFlag:  # if sunlight becomes available
            print("Auto: Sunlight! START rotating disk")
        elif rotateFlag_old and not rotateFlag:
            print("Auto: No Sunlight! STOP Rotating")


        return waterFlag, rotateFlag

    except:
        return waterFlag, rotateFlag


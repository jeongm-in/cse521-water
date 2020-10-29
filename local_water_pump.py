import time
import RPi.GPIO as GPIO

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


def config():
    para = dict()

    GPIO.cleanup()
    i2c = busio.I2C(board.SCL, board.SDA)
    para['ads'] = ADS.ADS1115(i2c)

    para['pinMoisSens'] = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(para['pinMoisSens'], GPIO.OUT)

    return para


def reading_sensors(para):
    readMoisSens = AnalogIn(para['ads'], ADS.P1).voltage

    if readMoisSens > 2.4:
        GPIO.output(para['pinMoisSens'], 1)
        print('Dry soil. water the flower ASAP \nCurrent moisture: {:.2f}'
              .format(readMoisSens))
    else:
        GPIO.output(para['pinMoisSens'], 0)
        print('The soil is fine now \nCurrent moisture: {:.2f}'
              .format(readMoisSens))


def main():
    para = config()

    for i in range(100):
        reading_sensors(para)

        time.sleep(1)

    GPIO.cleanup()


if __name__ == "__main__":
    main()

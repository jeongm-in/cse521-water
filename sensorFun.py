import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO

def pinMap():
    para = dict()

    i2c = busio.I2C(board.SCL, board.SDA)
    para['ads'] = ADS.ADS1115(i2c)

    para['pinPump'] = 21
    para['pinDisc'] = 26

    return para

"""
config sensors
"""
def sensorConfig():
    # GPIO.cleanup()
    para = pinMap()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(para['pinPump'], GPIO.OUT)
    GPIO.setup(para['pinDisc'], GPIO.OUT)
    GPIO.output(para['pinPump'], 0)
    GPIO.output(para['pinDisc'], 0)

    return dict(), [], []



def sensorReading(para):
    """
    read data sensors
    """
    reading = {}
    reading['mois'] = AnalogIn(para['ads'], ADS.P1).voltage
    reading['uv'] = AnalogIn(para['ads'], ADS.P2).voltage

    return reading
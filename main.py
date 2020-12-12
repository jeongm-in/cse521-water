import time

import helperFun as hf
import awsFun as af
import sensorFun as sf



# specify the period as integer second
sensorReadPeriod = 1  # 1 sec
awsSendPeriod = 5     # 5 sec
# awsListenPeriod = 5   # 5 sec


def main():
    para = sf.pinMap()
    sf.sensorConfig()
    awsClient, toIotTopic = af.awsConfig()

    data = dict()
    moisDataList = []
    UVDataList = []

    
    tCollectData = hf.RepeatedTimer(sensorReadPeriod, hf.collectData, para, moisDataList, UVDataList, data)
    tSendData = hf.RepeatedTimer(awsSendPeriod, hf.sendData, awsClient, toIotTopic, data, moisDataList, UVDataList)
    
    tCollectData.joinEnable(True)

    waterFlag_old = hf.waterFlag
    rotateFlag_old = hf.rotateFlag

    # desired_hum = 50

    while True:

        while hf.autoMode:     # in auto mode
            waterFlag_old, rotateFlag_old = hf.autoBehave(moisDataList, UVDataList, hf.desired_hum, waterFlag_old, rotateFlag_old)

            time.sleep(.5)
            print(hf.desired_hum)
        while not hf.autoMode: # in manual mode

            time.sleep(.5)
            print("manual mode")



if __name__ == "__main__":
    main()

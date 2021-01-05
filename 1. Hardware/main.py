import time

import helperFun as hf
import awsFun as af
import sensorFun as sf



# specify the period as integer second
sensorReadPeriod = 1    # 1 sec
awsSendPeriod = 5       # 5 sec
rotatePeriod = 0.005     # 0.01 sec, for rotating disk



def main():
    # some configuration
    para = sf.pinMap()
    data, moisDataList, UVDataList = sf.sensorConfig()
    awsClient, toIotTopic = af.awsConfig()

    # initial some var
    waterFlag_old = hf.waterFlag
    rotateFlag_old = hf.rotateFlag
    disk = hf.DiskRotation(para['pinDisc'])

    # initial timer
    tCollectData = hf.RepeatedTimer(sensorReadPeriod, hf.collectData, para, moisDataList, UVDataList, data)
    tCollectData.joinEnable(True)

    tSendData = hf.RepeatedTimer(awsSendPeriod, hf.sendData, awsClient, toIotTopic, data, moisDataList, UVDataList)

    tDisk = hf.RepeatedTimer(rotatePeriod, disk.rotate)
    tDisk.stop()


    while True:

        while hf.autoMode:     # in auto mode
            waterFlag_old, rotateFlag_old = hf.autoBehave(moisDataList, UVDataList, hf.desired_hum, waterFlag_old, rotateFlag_old)

            if hf.rotateFlag and not tDisk.is_running:
                tDisk._run()
            elif not hf.rotateFlag and tDisk.is_running:
                tDisk.stop()

            time.sleep(.5)
            # print(hf.desired_hum)
        while not hf.autoMode: # in manual mode
            if hf.rotateFlag and not tDisk.is_running:
                tDisk._run()
            elif not hf.rotateFlag and tDisk.is_running:
                tDisk.stop()

            time.sleep(.5)



if __name__ == "__main__":
    main()

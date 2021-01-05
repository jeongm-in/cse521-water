<?php


namespace Console;
use DB;


class ConsoleController
{
    var $output = null;
    public function __construct($mdb, $post)
    {
        $inputData = json_decode(strip_tags($post),true);
        If($inputData['cmd']=="getHistory"){
            $mdb->query("SET time_zone = '-06:00'");
            $dbEntities = $mdb->query("
SELECT humidity,timestamp FROM watering ORDER BY timestamp DESC LIMIT 0, 10");
            //echo $dbEntities;
            $this->output=json_encode($dbEntities);

        }elseif ($inputData['cmd']=="getRealTime"){
            $mdb->query("SET time_zone = '-06:00'");
            $dbEntities = $mdb->query("SELECT humidity,timestamp,mode,sunlight FROM readings ORDER BY timestamp DESC LIMIT 0, 1");
            $this->output=json_encode($dbEntities);
    }elseif ($inputData['cmd']=="getHum12Hr"){
            //$mdb->query("SET time_zone = '-06:00'");
            $timeNow = date("Y-m-d H:i:s");
            $timeSub12= (new \DateTime())->modify('-12 hours')->getTimestamp();
            $timeSub12 = date("Y-m-d H:i:s", $timeSub12);
            $dbEntities = $mdb->query("SELECT humidity,timestamp,mode FROM readings WHERE timestamp BETWEEN '$timeSub12' AND '$timeNow'");
            //$dbEntities = $mdb->query("SELECT humidity,timestamp,mode FROM readings WHERE timestamp BETWEEN '2020-12-15 18:31:40' AND '2020-12-16 06:31:40'");
            //var_dump("SELECT humidity,timestamp,mode FROM watering WHERE timestamp BETWEEN '$timeSub12' AND '$timeNow'");

            $timeNow = date("Y-m-d H:i:s");
            $test = date("2020-12-16 00:00:01");
            $timeBucket=[[],[],[],[],[],[],[],[],[],[],[],[]]; // -12 to Now

            foreach ($dbEntities as $row)
            {
                $rowTime = $row["timestamp"];
                $rowHumidity = $row["humidity"];
                if ($rowTime != NULL){
                    $timeDiff = abs(strtotime($timeNow) - strtotime($rowTime))/60;
                    if($timeDiff <=30)
                    {
                        array_push($timeBucket[11],(int)$rowHumidity);
                    }
                    if(30 < $timeDiff && $timeDiff <= 90)
                    {
                        array_push($timeBucket[10],(int)$rowHumidity);
                    }

                    if(90 < $timeDiff && $timeDiff <= 150)
                    {
                        array_push($timeBucket[9],(int)$rowHumidity);
                    }
                    if(150 < $timeDiff && $timeDiff <= 210)
                    {
                        array_push($timeBucket[8],(int)$rowHumidity);
                    }
                    if(210 < $timeDiff && $timeDiff <= 270)
                    {
                        array_push($timeBucket[7],(int)$rowHumidity);
                    }
                    if(270 < $timeDiff && $timeDiff <= 330)
                    {
                        array_push($timeBucket[6],(int)$rowHumidity);
                    }
                    if(330 < $timeDiff && $timeDiff <= 390)
                    {
                        array_push($timeBucket[5],(int)$rowHumidity);
                    }
                    if(390 < $timeDiff && $timeDiff <= 450)
                    {
                        array_push($timeBucket[4],(int)$rowHumidity);
                    }
                    if(450 < $timeDiff && $timeDiff <= 510)
                    {
                        array_push($timeBucket[3],(int)$rowHumidity);
                    }
                    if(510 < $timeDiff && $timeDiff <= 570)
                    {
                        array_push($timeBucket[2],(int)$rowHumidity);
                    }
                    if(570 < $timeDiff && $timeDiff <= 630)
                    {
                        array_push($timeBucket[1],(int)$rowHumidity);
                    }
                    if(630 < $timeDiff && $timeDiff <= 660)
                    {
                        array_push($timeBucket[0],(int)$rowHumidity);
                    }
                }
            }




            $timeBucket = $this->processArray($timeBucket);


            $this->output  = json_encode($timeBucket);
        }
        else{
            $this->execute($inputData['cmd'], $inputData['val']);
        }

    }

    private function processArray($array){
        $newArray=[];
        foreach($array as $key=>$value) {
            if(count($array[$key]) != 0){
            $array[$key] = round(array_sum($array[$key]) / count($array[$key]),2);
        }else{
                $array[$key] = 0;
            }
        }
        return $array;
    }

    private function execute($mode,$val){
        $this->output = exec("/usr/bin/python3 /var/script/awsiot/pub_topic.py $mode $val 2>&1");
    }


    public function feedback(){

    return $this->output;
}
}
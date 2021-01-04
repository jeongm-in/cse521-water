<?php
require "./ConsoleController.php";
require "./meekrodb-2.3.1/db.class.php";

date_default_timezone_set('UTC');
$mdb = new MeekroDB('cse521.cqnqix2ptb6p.us-east-2.rds.amazonaws.com', 'admin', 'cse521fl20', 'cse521', 3306);
//$mdb = new MeekroDB('ec2-54-84-170-41.compute-1.amazonaws.com', 'admin', 'cse521fl20', 'cse521', 3306);


$controller = new Console\ConsoleController($mdb, file_get_contents('php://input'));

echo $controller->feedback();
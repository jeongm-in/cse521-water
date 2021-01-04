import sys
import logging
import pymysql
from datetime import datetime
import time
import boto3

# Create an SNS client
sns = boto3.client('sns')



#rds settings
rds_host  = ""
name = ""
password = ""
db_name = ""
INTERVAL = 15
logger = logging.getLogger()
logger.setLevel(logging.INFO)
debug = False


try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def lambda_handler(event, context):
    print(event)
    pump_status = event.get('pump_status')
    current_humidity = event.get('Humidity')
    
    if not debug:
        # sleep(300)
        with conn.cursor() as cur:
            cur.execute(f'select humidity from readings where timestamp > now() - interval {INTERVAL} minute')
        
            result = [float(i[0]) for i in cur.fetchall()]
            if len(result) > 0:
                previous_humidity = sum(result)/len(result)
                previous_humidity = -1000
                if current_humidity < previous_humidity:
            
                    message = f'Your moisture level has not changed in the last {INTERVAL} minutes after pump activated. Please check the water tank.'
                    response = sns.publish(
                        TopicArn='arn:aws:sns:us-east-2:471367836706:cse521',    
                        Message=message, 
                    )
        
        conn.commit()
        return
    else:
        if True:
            previous_humidity = 100
            if True:
                message = f'Your moisture level has not changed in the last {INTERVAL} minutes after pump activated. Please check the water tank.'
                response = sns.publish(
                    TopicArn='arn:aws:sns:us-east-2:471367836706:cse521',    
                    Message=message, 
                )
        

    
    return

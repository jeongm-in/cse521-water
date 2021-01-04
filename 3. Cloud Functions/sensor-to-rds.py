import sys
import logging
import pymysql
from datetime import datetime
import time

#rds settings
rds_host  = ""
name = ""
password = ""
db_name = ""
F = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def lambda_handler(event, context):
    print(event)
    moisture = event.get('Humidity')
    sunlight = event.get("UV")
    
    timestamp_obj = datetime.fromisoformat(event.get('time'))
    timestamp = timestamp_obj.strftime(F)
    print(moisture,sunlight,timestamp)
    mode = 0

    print(timestamp)
    with conn.cursor() as cur:
        cur.execute(f'insert into readings (humidity, sunlight, timestamp, mode) values({moisture},{sunlight},"{timestamp}", {mode})')       
    
        conn.commit()
        # debug message
        # cur.execute("select * from readings")
        # for row in cur:
        #     item_count += 1
        #     logger.info(row)
        #     print(row)
    conn.commit()
    return
import redis
import pymongo
import json
from datetime import datetime

def connect_to_redis():
    return redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

def connect_to_mongo():
    client = pymongo.MongoClient('mongodb://mongo:27017')
    return client.border_alerts

def process_alerts():
    redis_conn = connect_to_redis()
    db = connect_to_mongo()
    while True:
        alert_data = redis_conn.lpop('urgent_queue') or redis_conn.lpop('normal_queue')
        if alert_data:
            alert = json.loads(alert_data)
            alert['insertion_time'] = datetime.utcnow().isoformat()
            db.alerts.insert_one(alert)

if __name__ == '__main__':
    process_alerts()

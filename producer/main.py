import json
import redis
from priority_logic import determine_priority

def connect_to_redis():
    return redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

def load_alerts(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def process_alerts(alerts):
    redis_conn = connect_to_redis()
    for alert in alerts:
        priority = determine_priority(alert)
        alert['priority'] = priority
        queue_name = 'urgent_queue' if priority == 'URGENT' else 'normal_queue'
        redis_conn.rpush(queue_name, json.dumps(alert))

if __name__ == '__main__':
    alerts = load_alerts('border_alerts.json')
    process_alerts(alerts)

import json
from priority_logic import determine_priority
from redis_connection import connect_to_redis


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
    alerts = load_alerts('/data/border_alerts.json')
    process_alerts(alerts)

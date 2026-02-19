import json
import pymongo
import redis

def connect_to_mongo():
    client = pymongo.MongoClient('mongodb://mongo:27017')
    return client.border_alerts

def connect_to_redis():
    return redis.Redis(host='redis', port=6379, db=0)

def cache_result(func):
    def wrapper():
        redis_conn = connect_to_redis()
        cache_key = f"cache:{func.__name__}"
        cached_result = redis_conn.get(cache_key)
        if cached_result:
            return json.loads(cached_result)
        result = func()
        redis_conn.set(cache_key, json.dumps(result), ex=300) 
        return result
    return wrapper

@cache_result
def get_alerts_by_border_and_priority():
    db = connect_to_mongo()
    pipeline = [
        {'$group': {'_id': {'border': '$border', 'priority': '$priority'}, 'count': {'$sum': 1}}}
    ]
    return list(db.alerts.aggregate(pipeline))

@cache_result
def get_top_urgent_zones():
    db = connect_to_mongo()
    pipeline = [
        {'$match': {'priority': 'URGENT'}},
        {'$group': {'_id': '$zone', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 5}
    ]
    return list(db.alerts.aggregate(pipeline))

@cache_result
def get_distance_distribution():
    db = connect_to_mongo()
    pipeline = [
        {'$bucket': {
            'groupBy': '$distance_from_fence_m',
            'boundaries': [0, 300, 800, 1500],
            'output': {'count': {'$sum': 1}}
        }}
    ]
    return list(db.alerts.aggregate(pipeline))



import redis

def connect_to_redis():
    return redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
import redis, os


# Redis Pool for Sessions
redis_pool_session = redis.ConnectionPool(
    host=os.getenv('REDIS_HOST'), 
    port=os.getenv('REDIS_PORT'), 
    db=os.getenv('REDIS_DB_SESSION'), 
    password=os.getenv('REDIS_PASSWORD'), 
    decode_responses=True
)

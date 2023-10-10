import redis 

class redisclient():
    def __init__(self) -> None:
        self.redis_host = 'localhost'
        self.redis_port = 6379
        self.redis_db = 0
        self.redis_client = redis.Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
    
import os

import redis
from rq import Worker, Queue, Connection

listen = ['default']

#redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
#redis_url = os.getenv('REDISTOGO_URL', 'redis://elasticache-redis.vs9dei.ng.0001.use2.cache.amazonaws.com:6379') #local redis old
redis_url = os.getenv('REDISTOGO_URL', 'redis://elasticache-redis.vs9dei.ng.0001.use2.cache.amazonaws.com:6379') #local redis new
#redis_url = os.getenv('REDISTOGO_URL', 'redis://co2gasponlineredisv2.vs9dei.ng.0001.use2.cache.amazonaws.com:6379') #remote redis



conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
import os

from redis import Redis

conn = Redis(f"{os.getenv('REDIS_URI')}")

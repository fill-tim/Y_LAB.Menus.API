import os

from dotenv import load_dotenv
from redis.asyncio import Redis

load_dotenv()

REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_HOST = os.getenv('REDIS_HOST')


async def get_redis():
    try:
        redis = await Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        return redis
    except Exception as error:
        print(error)

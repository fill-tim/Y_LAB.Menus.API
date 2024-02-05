import os

from dotenv import load_dotenv
from redis.asyncio import Redis

load_dotenv()

TEST_REDIS_PORT = os.getenv('TEST_REDIS_PORT')
TEST_REDIS_HOST = os.getenv('TEST_REDIS_HOST')


async def override_get_redis():
    try:
        redis = await Redis(host=TEST_REDIS_HOST, port=TEST_REDIS_PORT, db=0)
        return redis
    except Exception as error:
        print(error)

import os
from redis.asyncio import Redis
from dotenv import load_dotenv

load_dotenv()

TEST_REDIS_PORT = os.getenv("TEST_REDIS_PORT")
TEST_REDIS_HOST = os.getenv("TEST_REDIS_HOST")


async def override_get_redis():
    try:
        redis = await Redis(host=TEST_REDIS_HOST, port=TEST_REDIS_PORT, db=0)
        return redis
    except Exception as error:
        print(error)

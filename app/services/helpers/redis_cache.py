import json
from uuid import UUID

from fastapi import Depends
from redis.asyncio import Redis

from ...core import get_redis


class RedisCache:
    def __init__(self, rd: Redis = Depends(get_redis)) -> None:
        self._rd = rd

    async def get_value(self, tag: UUID | str) -> bytes | None:
        try:
            key = await self._rd.scan(match=f"{tag}*")

            if key[1] == []:
                return None

            return await self._rd.get(key[1][0])

        except Exception as error:
            print(error)

    async def set_value(
        self,
        key: str,
        value: str,
        tags: list | None = None,
    ):
        try:
            if tags:
                tags_str = "{" + ",".join(str(x) for x in tags) + "}"
            else:
                tags_str = ""

            await self._rd.set(f"{str(key)}" + f"{tags_str}", str(value))

        except Exception as error:
            print(error)

    async def del_cache(self, tags: list):
        try:
            if tags:
                for tag in tags:
                    caches = await self._rd.scan(match=f"*{tag}*")

                    if caches[1] is not []:
                        for key in caches[1]:
                            await self._rd.delete(key.decode("utf-8"))

        except Exception as error:
            print(error)

    async def convert_to_json(self, cache: bytes):
        try:
            return json.loads(cache.decode("utf-8").replace("'", '"'))
        except Exception as error:
            print(error)

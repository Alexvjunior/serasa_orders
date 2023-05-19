from typing import Optional

import aioredis
from django.conf import settings


class Cache:
    def __init__(self) -> None:
        self._redis = None

    async def setup(self) -> None:
        if not self._redis:
            self.redis = await aioredis.create_redis_pool(settings.REDIS_URL)

    async def get_cache(self, key: str) -> Optional[str]:
        await self.setup()

        value = await self.redis.get(key)

        if not value:
            return value

        return value.decode()

    async def delete_cache(self, key: str) -> None:
        await self.setup()
        await self.redis.delete(key)

    async def create_cache(self, key: str, value: any) -> None:
        await self.setup()
        await self.redis.set(key, value)

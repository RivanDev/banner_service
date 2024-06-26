import pickle

from redis import asyncio as aioredis

from application.core.config import settings


class CacheRepo:
    def __init__(self):
        self.redis_pool = aioredis.ConnectionPool.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0")
        self.cacher = aioredis.Redis(connection_pool=self.redis_pool)

    async def create_cache(self, key, value):
        await self.cacher.set(key, pickle.dumps(value), ex=settings.EXPIRATION)

    async def read_cache(self, key):
        data = await self.cacher.get(key)
        data_object = pickle.loads(data)
        return data_object

    async def update_cache(self, key, value):
        await self.cacher.set(key, pickle.dumps(value), ex=settings.EXPIRATION)

    async def delete_cache(self, key):
        await self.cacher.delete(key)

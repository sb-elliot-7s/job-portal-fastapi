import aioredis


class RedisService:
    def __init__(self):
        self.redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)

    async def write(self, key: str, value: str, ex: int):
        await self.redis.set(key, value, ex=ex)

    async def read(self, key: str):
        return await self.redis.get(key)

import redis.asyncio as aioredis
from cache.redis.pool import redis_pool


async def get_session() -> aioredis.Redis:
    return aioredis.Redis(connection_pool=redis_pool)  # TODO add closing

import redis.asyncio as aioredis
from common.settings import settings


redis_pool = aioredis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)
print("init redis pool")

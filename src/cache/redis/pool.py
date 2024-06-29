import logging
import redis.asyncio as aioredis
from common.settings import settings

logger = logging.getLogger("cache.pool")

redis_pool = aioredis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)
logger.info("pool created")

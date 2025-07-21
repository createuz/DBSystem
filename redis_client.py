from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from logger import logger
from settings import settings

redis: Redis  # global obyekti


async def init_redis():
    global redis
    pool = ConnectionPool.from_url(
        settings.REDIS_URL,
        max_connections=settings.REDIS_POOL_MAX_CONNECTIONS
    )
    redis = Redis(connection_pool=pool)
    # Ping orqali ulanishni tekshiramiz
    await redis.ping()
    logger.info("✅ Redis connected", redis_url=settings.REDIS_URL)


async def close_redis():
    await redis.close()
    logger.info("🛑 Redis connection closed")

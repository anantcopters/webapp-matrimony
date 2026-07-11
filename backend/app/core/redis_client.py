import os

from redis.asyncio import Redis
from redis.exceptions import RedisError


REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://127.0.0.1:6379/0",
)

redis_client = Redis.from_url(
    REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3,
    health_check_interval=30,
)


async def test_redis_connection() -> bool:
    try:
        return bool(await redis_client.ping())
    except RedisError:
        return False
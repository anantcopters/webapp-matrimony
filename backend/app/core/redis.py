"""Shared Redis connection pool."""

from redis.asyncio import Redis

from app.core.config import get_settings

settings = get_settings()

# Reuse Redis connections rather than reconnecting on every request.
redis_client = Redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3,
    health_check_interval=30,
)
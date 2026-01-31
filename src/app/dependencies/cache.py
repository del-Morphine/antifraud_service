from redis import Redis
from functools import lru_cache
from app.config import get_settings


@lru_cache
def get_cache() -> Redis:
    settings = get_settings()
    return Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        decode_responses=True,
    )
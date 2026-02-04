from functools import lru_cache

from upstash_redis.asyncio import Redis as AsyncRedis

from infra.settings import settings


@lru_cache
def _create_redis_client() -> AsyncRedis | None:
    if not settings.CACHE_ENABLED:
        return None

    has_credentials = (
        settings.UPSTASH_REDIS_REST_URL and settings.UPSTASH_REDIS_REST_TOKEN
    )
    if not has_credentials:
        return None

    return AsyncRedis(
        url=settings.UPSTASH_REDIS_REST_URL,
        token=settings.UPSTASH_REDIS_REST_TOKEN,
    )


def get_redis_client() -> AsyncRedis | None:
    return _create_redis_client()

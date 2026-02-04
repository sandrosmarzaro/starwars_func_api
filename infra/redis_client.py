from functools import lru_cache

from upstash_redis import Redis

from infra.settings import settings


@lru_cache
def _create_redis_client() -> Redis | None:
    if not settings.CACHE_ENABLED:
        return None

    has_credentials = (
        settings.UPSTASH_REDIS_REST_URL and settings.UPSTASH_REDIS_REST_TOKEN
    )
    if not has_credentials:
        return None

    return Redis(
        url=settings.UPSTASH_REDIS_REST_URL,
        token=settings.UPSTASH_REDIS_REST_TOKEN,
    )


def get_redis_client() -> Redis | None:
    return _create_redis_client()

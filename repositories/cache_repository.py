import json
from typing import Annotated

from fastapi import Depends
from loguru import logger
from upstash_redis import Redis

from infra.redis_client import get_redis_client
from infra.settings import settings
from schemas.swapi_query_params_schema import SwapiQueryParams


class CacheRepository:
    CACHE_PREFIX = 'swapi:v1'

    def __init__(
        self,
        client: Annotated[Redis | None, Depends(get_redis_client)],
    ) -> None:
        self.client = client
        self.ttl = settings.CACHE_TTL_SECONDS
        self.enabled = settings.CACHE_ENABLED and self.client is not None

    def build_cache_key(self, params: SwapiQueryParams) -> str:
        resource = params.resource.value
        item_id = str(params.id) if params.id else 'list'
        page = str(params.page) if params.page else '1'
        search = params.search or ''

        return f'{self.CACHE_PREFIX}:{resource}:{item_id}:{page}:{search}'

    def get(self, params: SwapiQueryParams) -> dict | None:
        if not self.enabled or self.client is None:
            return None

        cache_key = self.build_cache_key(params)

        try:
            cached_data = self.client.get(cache_key)
            if cached_data is not None:
                logger.debug(f'Cache HIT: {cache_key}')
                if isinstance(cached_data, str):
                    return json.loads(cached_data)
                return cached_data
            logger.debug(f'Cache MISS: {cache_key}')
        except (ConnectionError, TimeoutError, json.JSONDecodeError) as e:
            logger.warning(f'Cache GET error for {cache_key}: {e}')

        return None

    def set(self, params: SwapiQueryParams, data: dict) -> bool:
        if not self.enabled or self.client is None:
            return False

        cache_key = self.build_cache_key(params)

        try:
            self.client.set(cache_key, json.dumps(data), ex=self.ttl)
            logger.debug(f'Cache SET: {cache_key} (TTL: {self.ttl}s)')
        except (ConnectionError, TimeoutError) as e:
            logger.warning(f'Cache SET error for {cache_key}: {e}')
            return False
        else:
            return True

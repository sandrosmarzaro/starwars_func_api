from typing import Annotated
from urllib.parse import urljoin

import httpx
from fastapi import Depends
from loguru import logger

from infra.settings import settings
from repositories.cache_repository import CacheRepository
from schemas.swapi_query_params_schema import SwapiQueryParams
from services.expand_swapi_data_service import ExpandSwapiDataService
from services.sort_swapi_data_service import SortSwapiDataService


class SwapiDataService:
    def __init__(
        self,
        cache_repository: Annotated[CacheRepository, Depends()],
    ) -> None:
        self.base_url = settings.SWAPI_BASE_URL
        self.expand_service = ExpandSwapiDataService()
        self.sort_service = SortSwapiDataService()
        self.cache_repository = cache_repository

    async def get_swapi_data(
        self, params: SwapiQueryParams
    ) -> dict[str, object]:
        cached_data = self.cache_repository.get(params)
        if cached_data is not None:
            data = cached_data
        else:
            data = await self._fetch_from_swapi(params)
            self.cache_repository.set(params, data)

        if params.expand:
            async with httpx.AsyncClient() as client:
                data = await self.expand_service.expand(
                    client, data, params.expand
                )

        if params.sort_by:
            data = self.sort_service.sort(
                data, params.sort_by, params.sort_order
            )

        return data

    async def _fetch_from_swapi(
        self, params: SwapiQueryParams
    ) -> dict[str, object]:
        resource_url = urljoin(self.base_url, f'{params.resource.value}/')

        if params.id:
            resource_url = urljoin(resource_url, str(params.id))

        query_params: dict[str, str | int] = {}
        if params.search:
            query_params['search'] = params.search
        if params.page:
            query_params['page'] = params.page

        logger.debug(resource_url)
        async with httpx.AsyncClient() as client:
            response = await client.get(resource_url, params=query_params)
            response.raise_for_status()
            data = response.json()

        logger.debug(f'{response}, {data}')
        return data

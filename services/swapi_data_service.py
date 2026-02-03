from typing import Any
from urllib.parse import urljoin

import httpx
from loguru import logger

from infra.settings import settings
from schemas.swapi_query_params_schema import SwapiQueryParams
from services.expand_swapi_data_service import ExpandSwapiDataService


class SwapiDataService:
    def __init__(self) -> None:
        self.base_url = settings.SWAPI_BASE_URL
        self.expand_service = ExpandSwapiDataService()

    async def get_swapi_data(self, params: SwapiQueryParams) -> dict[str, Any]:
        resource_url = urljoin(self.base_url, f'{params.resource}/')

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

            if params.expand:
                data = await self.expand_service.expand(client, data)

        logger.debug(f'{response}, {data}')
        return data

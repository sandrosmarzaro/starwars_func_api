import asyncio
from typing import Any, ClassVar

import httpx
from loguru import logger


class ExpandSwapiDataService:
    _skip_fields: ClassVar[set[str]] = {
        'url',
        'next',
        'previous',
        'created',
        'edited',
    }

    async def expand(
        self, client: httpx.AsyncClient, data: dict[str, Any]
    ) -> dict[str, Any]:
        if 'results' not in data:
            return await self._expand_item(client, data)

        data['results'] = list(
            await asyncio.gather(
                *[self._expand_item(client, i) for i in data['results']]
            )
        )
        return data

    async def _expand_item(
        self, client: httpx.AsyncClient, item: dict[str, Any]
    ) -> dict[str, Any]:
        async def fetch(url: str) -> dict[str, Any]:
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPError:
                logger.warning(f'Failed to fetch {url}')
                return {'url': url, 'error': 'Failed to fetch resource'}

        async def fetch_many(urls: list[str]) -> list[dict[str, Any]]:
            return list(await asyncio.gather(*[fetch(u) for u in urls]))

        def make_task(val: object) -> asyncio.Task[Any] | None:
            match val:
                case str() if val.startswith('http'):
                    return asyncio.create_task(fetch(val))
                case list() if val and all(
                    isinstance(v, str) and v.startswith('http') for v in val
                ):
                    return asyncio.create_task(fetch_many(val))
            return None

        tasks = {
            k: task
            for k, v in item.items()
            if k not in self._skip_fields and (task := make_task(v))
        }

        results = await asyncio.gather(*tasks.values())
        return item | dict(zip(tasks.keys(), results, strict=True))

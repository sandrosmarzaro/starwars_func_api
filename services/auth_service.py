from typing import Annotated

from fastapi import Security
from fastapi.security import APIKeyHeader

from exceptions.errors import UnauthorizedError
from infra.settings import settings

api_key_header = APIKeyHeader(name='X-API-Key', auto_error=False)


async def verify_api_key(
    api_key: Annotated[str | None, Security(api_key_header)],
) -> str:
    if api_key is None:
        raise UnauthorizedError(message='X-API-Key header missing')
    if api_key != settings.API_KEY:
        raise UnauthorizedError(message='Invalid API key')
    return api_key

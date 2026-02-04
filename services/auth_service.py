from typing import Annotated

from fastapi import Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name='X-API-Key', auto_error=False)


async def verify_api_key(
    api_key: Annotated[str, Security(api_key_header)],
) -> str:
    return api_key

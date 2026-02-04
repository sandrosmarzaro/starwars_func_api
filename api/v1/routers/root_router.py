from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends

from exceptions.errors import InternalServerError, UnauthorizedError
from infra.settings import settings
from schemas.root_schema import RootResponse
from schemas.swapi_query_params_schema import SwapiResource
from services.auth_service import verify_api_key

ROOT_RESPONSES: dict[int | str, dict[str, Any]] = {
    HTTPStatus.UNAUTHORIZED: {
        'model': UnauthorizedError.schema(),
        'description': 'Invalid or missing API key',
    },
    HTTPStatus.INTERNAL_SERVER_ERROR: {
        'model': InternalServerError.schema(),
        'description': 'Internal server error',
    },
}

router = APIRouter(tags=['root'], dependencies=[Depends(verify_api_key)])


@router.get(
    '/',
    summary='API Root',
    description='Lists all available API resources and endpoints.',
    response_description='Available API endpoints',
    responses=ROOT_RESPONSES,
)
async def get_root() -> RootResponse:
    base_url = settings.API_GATEWAY_URL.rstrip('/')
    swapi_url = f'{base_url}/api/v1/swapi?resource='
    return RootResponse(
        documentation=f'{base_url}/docs',
        **{r.value: f'{swapi_url}{r.value}' for r in SwapiResource},
    )

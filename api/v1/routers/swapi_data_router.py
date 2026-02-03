from http import HTTPStatus
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from exceptions.errors import (
    BadRequestError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    UnprocessableEntityError,
)
from schemas.examples.swapi_router_examples import SWAPI_EXAMPLES
from schemas.swapi_query_params_schema import SwapiQueryParams
from services.auth_service import verify_api_key
from services.swapi_data_service import SwapiDataService

SWAPI_RESPONSES: dict[int | str, dict[str, Any]] = {
    HTTPStatus.UNAUTHORIZED: {
        'model': UnauthorizedError.schema(),
        'description': 'Invalid or missing API key',
    },
    HTTPStatus.NOT_FOUND: {
        'model': NotFoundError.schema(),
        'description': 'Resource not found in SWAPI',
    },
    HTTPStatus.BAD_REQUEST: {
        'model': BadRequestError.schema(),
        'description': 'Invalid request to SWAPI',
    },
    HTTPStatus.INTERNAL_SERVER_ERROR: {
        'model': InternalServerError.schema(),
        'description': 'Internal server error',
    },
    HTTPStatus.UNPROCESSABLE_ENTITY: {
        'model': UnprocessableEntityError.schema(),
        'description': 'Unprocessable entity',
    },
}

router = APIRouter(
    prefix='/swapi',
    tags=['swapi'],
    dependencies=[Depends(verify_api_key)],
)


@router.get(
    '/',
    summary='Query SWAPI resources',
    description='Fetch data from Star Wars API. '
    'Supports listing, filtering by ID, searching, and pagination.',
    response_description='SWAPI resource data',
    responses=SWAPI_RESPONSES,
)
async def get_swapi_data(
    service: Annotated[SwapiDataService, Depends()],
    params: Annotated[
        SwapiQueryParams, Query(openapi_examples=SWAPI_EXAMPLES)
    ],
) -> dict[str, Any]:
    return await service.get_swapi_data(params)

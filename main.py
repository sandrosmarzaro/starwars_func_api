from urllib.parse import urljoin

import functions_framework.aio
import httpx
from httpx import HTTPError
from loguru import logger
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import Response

from exceptions.error_handler import (
    handle_api_error,
    handle_httpx_error,
    handle_validation_error,
)
from exceptions.errors import BaseError
from infra.settings import settings
from utils.response import api_response, cors_preflight_response
from validators.request_validator import RequestValidator


@functions_framework.aio.http
async def starwars_func(request: Request) -> Response:
    params = dict(request.query_params)
    logger.debug(f'{request.url.path}, {params}')

    if request.method == 'OPTIONS':
        return cors_preflight_response()

    try:
        RequestValidator.validate(request)
        return await _get_swapi_data(params)
    except BaseError as exc:
        return handle_api_error(exc)
    except ValidationError as exc:
        return handle_validation_error(exc)
    except HTTPError as exc:
        return handle_httpx_error(exc)


async def _get_swapi_data(params: dict) -> Response:
    resource = params.get('resource')
    resource_id = params.get('id')
    base_url = urljoin(settings.SWAPI_BASE_URL, f'{resource}/')

    if resource_id:
        base_url = urljoin(base_url, resource_id)

    query_params = {
        key: params[key] for key in ('search', 'page') if params.get(key)
    }

    logger.debug(base_url)
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=query_params)
        response.raise_for_status()

    logger.debug(f'{response}, {response.json()}')
    return api_response(response.json())

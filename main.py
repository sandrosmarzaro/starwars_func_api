from urllib.parse import urljoin

import functions_framework
import httpx
from flask import Request
from loguru import logger

from exceptions import error_handler
from infra.settings import settings
from models.api_response import ApiResponse
from utils.response import api_response, cors_preflight_response
from validators.request_validator import RequestValidator

error_handler.setup()


@functions_framework.http
def starwars_func(request: Request) -> ApiResponse:
    logger.debug(f'{request.path}, {request.args}')

    if request.method == 'OPTIONS':
        return cors_preflight_response()

    RequestValidator.validate(request)

    return _get_swapi_data(request.args)


def _get_swapi_data(params: dict) -> ApiResponse:
    resource = params.get('resource')
    resource_id = params.get('id')
    base_url = urljoin(settings.SWAPI_BASE_URL, f'{resource}/')

    if resource_id:
        base_url = urljoin(base_url, resource_id)

    query_params = {
        key: params[key] for key in ('search', 'page') if params.get(key)
    }

    logger.debug(base_url)
    with httpx.Client() as client:
        response = client.get(base_url, params=query_params)
        response.raise_for_status()

    logger.debug(f'{response}, {response.json()}')
    return api_response(response.json())

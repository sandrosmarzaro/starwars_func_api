from http import HTTPStatus
from urllib.parse import urljoin

import functions_framework
import httpx
from flask import Request, Response, jsonify
from loguru import logger

from infra.settings import settings
from validators.request_validator import RequestValidator


@functions_framework.http
def starwars_func(request: Request) -> tuple[Response, int, dict]:
    logger.debug(f'{request.path}, {request.args}')

    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
        }
        return (jsonify({}), HTTPStatus.NO_CONTENT.value, headers)

    headers = {'Access-Control-Allow-Origin': '*'}

    is_valid_request, error = RequestValidator.validate(request)
    if not is_valid_request and error is not None:
        return (jsonify(error.to_dict()), error.status, headers)

    swapi_data = _get_swapi_data(request.args)

    return (swapi_data, HTTPStatus.OK.value, headers)


def _get_swapi_data(params: dict) -> Response:
    resource = params.get('resource')
    resource_id = params.get('id')
    base_url = urljoin(settings.SWAPI_BASE_URL, resource)

    if resource_id:
        base_url = urljoin(base_url, resource_id)

    query_params = {
        key: params[key] for key in ('search', 'page') if params.get(key)
    }

    with httpx.Client() as client:
        response = client.get(base_url, params=query_params)
        response.raise_for_status()

    logger.debug(f'{response}, {response.json()}')
    return jsonify(response.json())

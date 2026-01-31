from http import HTTPStatus
from urllib.parse import urljoin

import functions_framework
import httpx
from flask import Request, Response, jsonify
from httpx import HTTPStatusError
from loguru import logger

from exceptions.errors import (
    BadRequestError,
    InternalServerError,
    MethodNotAllowedError,
    NotFoundError,
)
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

    swapi_data, status = _get_swapi_data(request.args)

    return (swapi_data, status, headers)


def _get_swapi_data(params: dict) -> tuple[Response, int]:
    resource = params.get('resource')
    resource_id = params.get('id')
    base_url = urljoin(settings.SWAPI_BASE_URL, f'{resource}/')

    if resource_id:
        base_url = urljoin(base_url, resource_id)

    query_params = {
        key: params[key] for key in ('search', 'page') if params.get(key)
    }

    logger.debug(base_url)
    try:
        with httpx.Client() as client:
            response = client.get(base_url, params=query_params)
            response.raise_for_status()
    except HTTPStatusError as exc:
        logger.error(exc)
        status_code = exc.response.status_code

        error_mapping = {
            HTTPStatus.NOT_FOUND.value: NotFoundError,
            HTTPStatus.BAD_REQUEST.value: BadRequestError,
            HTTPStatus.METHOD_NOT_ALLOWED.value: MethodNotAllowedError,
        }
        error_class = error_mapping.get(status_code, InternalServerError)
        error = error_class()

        return (jsonify(error.to_dict()), error.status)

    logger.debug(f'{response}, {response.json()}')
    return (jsonify(response.json()), HTTPStatus.OK.value)

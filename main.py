from http import HTTPStatus

import functions_framework
from flask import Request, Response, jsonify
from loguru import logger

from validators.request_validator import RequestValidator


@functions_framework.http
def starwars_func(request: Request) -> tuple[Response, int, dict]:
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
        }
        return (jsonify({}), HTTPStatus.NO_CONTENT.value, headers)

    headers = {'Access-Control-Allow-Origin': '*'}

    logger.debug(request.path)

    is_valid_request, error = RequestValidator.validate(request)
    if not is_valid_request and error is not None:
        return (error.to_response(), error.status, headers)

    return (jsonify({'message': 'Hello World!'}), HTTPStatus.OK.value, headers)

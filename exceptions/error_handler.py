from http import HTTPStatus

import functions_framework
from flask import Flask
from httpx import HTTPError, HTTPStatusError
from loguru import logger
from pydantic import ValidationError

from exceptions.errors import (
    BadRequestError,
    BaseError,
    InternalServerError,
    MethodNotAllowedError,
    NotFoundError,
)
from models.api_response import ApiResponse
from utils.response import error_response

_HTTP_EXCEPTION_MAPPING = {
    HTTPStatus.BAD_REQUEST.value: BadRequestError,
    HTTPStatus.NOT_FOUND.value: NotFoundError,
    HTTPStatus.METHOD_NOT_ALLOWED.value: MethodNotAllowedError,
    HTTPStatus.INTERNAL_SERVER_ERROR.value: InternalServerError,
}


def _create_error_from_httpx(exc: HTTPError) -> BaseError:
    if isinstance(exc, HTTPStatusError):
        status_code = exc.response.status_code
        error_class = _HTTP_EXCEPTION_MAPPING.get(
            status_code, InternalServerError
        )
        return error_class()

    return InternalServerError()


def _handle_httpx_error(exc: HTTPError) -> ApiResponse:
    logger.error(exc)
    error = _create_error_from_httpx(exc)
    return error_response(error)


def _handle_api_error(exc: BaseError) -> ApiResponse:
    logger.warning(exc)
    return error_response(exc)


def _handle_validation_error(exc: ValidationError) -> ApiResponse:
    logger.warning(exc)
    return error_response(BadRequestError())


def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(HTTPError, _handle_httpx_error)
    app.register_error_handler(BaseError, _handle_api_error)
    app.register_error_handler(ValidationError, _handle_validation_error)


@functions_framework.errorhandler(HTTPError)
def handle_httpx_errors(exc: HTTPError) -> ApiResponse:
    return _handle_httpx_error(exc)


@functions_framework.errorhandler(BaseError)
def handle_api_erros(exc: BaseError) -> ApiResponse:
    return _handle_api_error(exc)


@functions_framework.errorhandler(ValidationError)
def handle_validation_error(exc: ValidationError) -> ApiResponse:
    return _handle_validation_error(exc)


def setup() -> None:
    pass

from http import HTTPStatus

from httpx import HTTPError, HTTPStatusError
from loguru import logger
from pydantic import ValidationError
from starlette.responses import Response

from exceptions.errors import (
    BadRequestError,
    BaseError,
    InternalServerError,
    MethodNotAllowedError,
    NotFoundError,
)
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


def handle_httpx_error(exc: HTTPError) -> Response:
    logger.error(exc)
    error = _create_error_from_httpx(exc)
    return error_response(error)


def handle_api_error(exc: BaseError) -> Response:
    logger.warning(exc)
    return error_response(exc)


def handle_validation_error(exc: ValidationError) -> Response:
    logger.warning(exc)
    return error_response(BadRequestError())

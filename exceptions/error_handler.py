from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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


async def __handle_base_error(
    request: Request,  # noqa: ARG001
    exc: BaseError,
) -> JSONResponse:
    logger.warning(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={'error': type(exc).__name__, 'detail': exc.message},
    )


async def __handle_httpx_error(
    request: Request,  # noqa: ARG001
    exc: HTTPError,
) -> JSONResponse:
    logger.error(exc)
    error = _create_error_from_httpx(exc)
    return JSONResponse(
        status_code=error.status_code,
        content={'error': type(error).__name__, 'detail': error.message},
    )


async def __global_internal_handle_error(
    request: Request,  # noqa: ARG001
    exc: Exception,
) -> JSONResponse:
    logger.error(exc)
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            'error': type(exc).__name__,
            'detail': HTTPStatus.INTERNAL_SERVER_ERROR.description,
        },
    )


async def __global_validation_handle_error(
    request: Request,  # noqa: ARG001
    exc: RequestValidationError,
) -> JSONResponse:
    logger.warning(exc)
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
        content={
            'error': type(exc).__name__,
            'detail': jsonable_encoder(exc.errors()),
        },
    )


async def __pydantic_validation_handle_error(
    request: Request,  # noqa: ARG001
    exc: ValidationError,
) -> JSONResponse:
    logger.warning(exc)
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
        content={
            'error': 'RequestValidationError',
            'detail': jsonable_encoder(exc.errors()),
        },
    )


def add_exceptions_handler(app: FastAPI) -> None:
    app.add_exception_handler(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        __global_internal_handle_error,
    )
    app.add_exception_handler(
        RequestValidationError,
        __global_validation_handle_error,  # pyright: ignore[reportArgumentType]
    )
    app.add_exception_handler(
        ValidationError,
        __pydantic_validation_handle_error,  # pyright: ignore[reportArgumentType]
    )
    app.add_exception_handler(
        BaseError,
        __handle_base_error,  # pyright: ignore[reportArgumentType]
    )
    app.add_exception_handler(
        HTTPError,
        __handle_httpx_error,  # pyright: ignore[reportArgumentType]
    )

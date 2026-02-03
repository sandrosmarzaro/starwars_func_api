from functools import lru_cache
from http import HTTPStatus
from typing import Any, Literal

from pydantic import BaseModel, create_model


class BaseError(Exception):
    def __init__(
        self,
        message: str | dict[str, Any],
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.headers = headers

    @classmethod
    @lru_cache
    def schema(cls) -> type[BaseModel]:
        return create_model(
            cls.__name__,
            error=(Literal[cls.__name__], ...),  # pyright: ignore[reportArgumentType]
            detail=(str | list[dict[str, Any]], ...),
        )


class MethodNotAllowedError(BaseError):
    def __init__(
        self,
        message: str = HTTPStatus.METHOD_NOT_ALLOWED.description,
        status_code: int = HTTPStatus.METHOD_NOT_ALLOWED,
    ) -> None:
        super().__init__(message, status_code)


class NotFoundError(BaseError):
    def __init__(
        self,
        message: str = HTTPStatus.NOT_FOUND.description,
        status_code: int = HTTPStatus.NOT_FOUND,
    ) -> None:
        super().__init__(message, status_code)


class BadRequestError(BaseError):
    def __init__(
        self,
        message: str = HTTPStatus.BAD_REQUEST.description,
        status_code: int = HTTPStatus.BAD_REQUEST,
    ) -> None:
        super().__init__(message, status_code)


class InternalServerError(BaseError):
    def __init__(
        self,
        message: str = HTTPStatus.INTERNAL_SERVER_ERROR.description,
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
    ) -> None:
        super().__init__(message, status_code)


class UnauthorizedError(BaseError):
    def __init__(
        self,
        message: str = HTTPStatus.UNAUTHORIZED.description,
        status_code: int = HTTPStatus.UNAUTHORIZED,
    ) -> None:
        super().__init__(message, status_code)


class UnprocessableEntityError(BaseError):
    def __init__(
        self,
        message: str = HTTPStatus.UNPROCESSABLE_ENTITY.description,
        status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY,
    ) -> None:
        super().__init__(message, status_code)

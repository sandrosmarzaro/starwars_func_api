from http import HTTPStatus


class BaseError(Exception):
    def __init__(self, name: str, message: str, status: int) -> None:
        super().__init__()
        self.name = name
        self.message = message
        self.status = status

    def to_dict(self) -> dict[str, str | int]:
        return {
            'error': self.name,
            'message': self.message,
            'status': self.status,
        }

    def __str__(self) -> str:
        return f'{self.name}(status={self.status},message={self.message})'


class MethodNotAllowedError(BaseError):
    def __init__(
        self,
        name: str = HTTPStatus.METHOD_NOT_ALLOWED.name,
        message: str = HTTPStatus.METHOD_NOT_ALLOWED.description,
        status: int = HTTPStatus.METHOD_NOT_ALLOWED.value,
    ) -> None:
        super().__init__(name, message, status)


class NotFoundError(BaseError):
    def __init__(
        self,
        name: str = HTTPStatus.NOT_FOUND.name,
        message: str = HTTPStatus.NOT_FOUND.description,
        status: int = HTTPStatus.NOT_FOUND.value,
    ) -> None:
        super().__init__(name, message, status)


class BadRequestError(BaseError):
    def __init__(
        self,
        name: str = HTTPStatus.BAD_REQUEST.name,
        message: str = HTTPStatus.BAD_REQUEST.description,
        status: int = HTTPStatus.BAD_REQUEST.value,
    ) -> None:
        super().__init__(name, message, status)


class InternalServerError(BaseError):
    def __init__(
        self,
        name: str = HTTPStatus.INTERNAL_SERVER_ERROR.name,
        message: str = HTTPStatus.INTERNAL_SERVER_ERROR.description,
        status: int = HTTPStatus.INTERNAL_SERVER_ERROR.value,
    ) -> None:
        super().__init__(name, message, status)

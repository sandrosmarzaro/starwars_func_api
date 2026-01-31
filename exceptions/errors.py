from http import HTTPStatus

from flask import Response, jsonify


class BaseError:
    name: str
    message: str
    status: int

    @classmethod
    def to_response(cls) -> Response:
        return jsonify(
            {
                'error': cls.name,
                'message': cls.message,
            }
        )

    def __repr__(self) -> str:
        return f'{self.name}(status={self.status},message={self.message})'


class MethodNotAllowedError(BaseError):
    name = HTTPStatus.METHOD_NOT_ALLOWED.name
    message = HTTPStatus.METHOD_NOT_ALLOWED.description
    status = HTTPStatus.METHOD_NOT_ALLOWED.value


class NotFoundError(BaseError):
    name = HTTPStatus.NOT_FOUND.name
    message = HTTPStatus.NOT_FOUND.description
    status = HTTPStatus.NOT_FOUND.value

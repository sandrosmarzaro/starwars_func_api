from flask import Request
from loguru import logger

from exceptions.errors import BaseError, MethodNotAllowedError, NotFoundError


class RequestValidator:
    @classmethod
    def validate(
        cls,
        request: Request,
    ) -> tuple[bool, type[BaseError] | None]:
        if request.method != 'GET':
            logger.warning(MethodNotAllowedError)
            return (False, MethodNotAllowedError)

        params = request.args
        resource = params.get('resource')

        resources = [
            'people',
            'planets',
            'starships',
            'films',
            'species',
            'vehicles',
        ]
        if not resource or resource not in resources:
            logger.warning(NotFoundError)
            return (False, NotFoundError)
        return (True, None)

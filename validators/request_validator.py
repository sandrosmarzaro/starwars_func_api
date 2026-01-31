from flask import Request
from loguru import logger
from pydantic import ValidationError

from exceptions.errors import (
    BadRequestError,
    BaseError,
    MethodNotAllowedError,
    NotFoundError,
)
from schemas.query_params_schema import SwapiQueryParams


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
        if not resource:
            logger.warning(BadRequestError)
            return (False, BadRequestError)
        resources = [
            'films',
            'people',
            'planets',
            'species',
            'starships',
            'vehicles',
        ]
        if resource not in resources:
            logger.warning(NotFoundError)
            return (False, NotFoundError)

        try:
            SwapiQueryParams.model_validate(request.args)
        except ValidationError:
            logger.warning(BadRequestError)
            return (False, BadRequestError)

        return (True, None)

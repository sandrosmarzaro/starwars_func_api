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
    ) -> tuple[bool, BaseError | None]:
        if request.method != 'GET':
            error = MethodNotAllowedError()
            logger.warning(error)
            return (False, error)

        params = request.args
        resource = params.get('resource')
        if not resource:
            error = BadRequestError()
            logger.warning(error)
            return (False, error)
        resources = [
            'films',
            'people',
            'planets',
            'species',
            'starships',
            'vehicles',
        ]
        if resource not in resources:
            error = NotFoundError()
            logger.warning(error)
            return (False, error)

        try:
            validated_params = SwapiQueryParams.model_validate(request.args)
        except ValidationError:
            error = BadRequestError()
            logger.warning(error)
            return (False, error)

        if validated_params.id is not None and (
            validated_params.search or validated_params.page
        ):
            error = BadRequestError()
            logger.warning(error)
            return (False, error)

        return (True, None)

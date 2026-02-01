from flask import Request
from loguru import logger

from exceptions.errors import MethodNotAllowedError
from schemas.query_params_schema import SwapiQueryParams


class RequestValidator:
    @classmethod
    def validate(
        cls,
        request: Request,
    ) -> None:
        if request.method != 'GET':
            raise MethodNotAllowedError

        SwapiQueryParams.model_validate(request.args)

        logger.debug('request validation ok')

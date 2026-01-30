from flask import Flask, request

from exceptions.errors import MethodNotAllowedError, NotFoundError
from validators.request_validator import RequestValidator


class TestRequestValidator:
    BASE_URL = '/'

    def test_should_error_with_different_method_from_get(
        self, app: Flask
    ) -> None:
        not_allowed_methods = [
            'POST',
            'PUT',
            'PATCH',
            'DELETE',
            'HEAD',
            'OPTIONS',
            'CONNECT',
            'TRACE',
        ]

        for method in not_allowed_methods:
            with app.test_request_context(
                f'{self.BASE_URL}?resource=people', method=method
            ):
                is_valid, error = RequestValidator.validate(request)

                assert is_valid is False
                assert error == MethodNotAllowedError

    def test_should_error_when_not_exist_resource(self, app: Flask) -> None:
        with app.test_request_context(
            f'{self.BASE_URL}?resource=nonexists', method='GET'
        ):
            is_valid, error = RequestValidator.validate(request)

            assert is_valid is False
            assert error == NotFoundError

    def test_validate_successful_request(self, app: Flask) -> None:
        valid_resources = [
            'films',
            'people',
            'planets',
            'species',
            'starships',
            'vehicles',
        ]
        for resource in valid_resources:
            with app.test_request_context(
                f'{self.BASE_URL}?resource={resource}', method='GET'
            ):
                is_valid, error = RequestValidator.validate(request)

                assert is_valid is True
                assert error is None

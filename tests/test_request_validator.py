from http import HTTPStatus

import pytest
from flask import Flask, request
from pydantic import ValidationError

from exceptions.errors import BadRequestError, MethodNotAllowedError
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
            with (
                app.test_request_context(
                    f'{self.BASE_URL}?resource=people', method=method
                ),
                pytest.raises(MethodNotAllowedError) as exc_info,
            ):
                RequestValidator.validate(request)

            assert exc_info.value.status == HTTPStatus.METHOD_NOT_ALLOWED.value
            assert (
                exc_info.value.to_dict() == MethodNotAllowedError().to_dict()
            )

    def test_should_error_when_not_exist_resource(self, app: Flask) -> None:
        with (
            app.test_request_context(
                f'{self.BASE_URL}?resource=nonexists', method='GET'
            ),
            pytest.raises(ValidationError) as exc_info,
        ):
            RequestValidator.validate(request)

        assert exc_info.value.error_count() == 1
        assert exc_info.value.errors()[0]['loc'] == ('resource',)
        assert exc_info.value.errors()[0]['type'] == 'literal_error'

    def test_should_error_when_not_passed_resource(self, app: Flask) -> None:
        with (
            app.test_request_context(f'{self.BASE_URL}', method='GET'),
            pytest.raises(ValidationError) as exc_info,
        ):
            RequestValidator.validate(request)

        assert exc_info.value.error_count() == 1
        assert exc_info.value.errors()[0]['loc'] == ('resource',)
        assert exc_info.value.errors()[0]['type'] == 'missing'

    def test_should_error_when_page_is_not_int(self, app: Flask) -> None:
        with (
            app.test_request_context(
                f'{self.BASE_URL}?resource=people&page=a', method='GET'
            ),
            pytest.raises(ValidationError) as exc_info,
        ):
            RequestValidator.validate(request)

        assert exc_info.value.error_count() == 1
        assert exc_info.value.errors()[0]['loc'] == ('page',)
        assert exc_info.value.errors()[0]['type'] == 'int_parsing'

    def test_should_error_when_id_is_not_int(self, app: Flask) -> None:
        with (
            app.test_request_context(
                f'{self.BASE_URL}?resource=people&id=a', method='GET'
            ),
            pytest.raises(ValidationError) as exc_info,
        ):
            RequestValidator.validate(request)

        assert exc_info.value.error_count() == 1
        assert exc_info.value.errors()[0]['loc'] == ('id',)
        assert exc_info.value.errors()[0]['type'] == 'int_parsing'

    def test_should_error_when_use_id_and_search(self, app: Flask) -> None:
        with (
            app.test_request_context(
                f'{self.BASE_URL}?resource=people&id=1&search=something',
                method='GET',
            ),
            pytest.raises(BadRequestError) as exc_info,
        ):
            RequestValidator.validate(request)

        assert exc_info.value.status == HTTPStatus.BAD_REQUEST.value
        assert exc_info.value.to_dict() == BadRequestError().to_dict()

    def test_should_error_when_use_id_and_page(self, app: Flask) -> None:
        with (
            app.test_request_context(
                f'{self.BASE_URL}?resource=people&id=1&page=2',
                method='GET',
            ),
            pytest.raises(BadRequestError) as exc_info,
        ):
            RequestValidator.validate(request)

        assert exc_info.value.status == HTTPStatus.BAD_REQUEST.value
        assert exc_info.value.to_dict() == BadRequestError().to_dict()

    def test_validate_successful_resources_request(self, app: Flask) -> None:
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
                RequestValidator.validate(request)

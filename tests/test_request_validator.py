from http import HTTPStatus

import pytest
from pydantic import ValidationError
from starlette.requests import Request

from exceptions.errors import BadRequestError, MethodNotAllowedError
from validators.request_validator import RequestValidator


def _build_request(path: str, method: str = 'GET') -> Request:
    scope = {
        'type': 'http',
        'method': method,
        'path': path.split('?')[0] if '?' in path else path,
        'query_string': (path.split('?')[1].encode() if '?' in path else b''),
        'headers': [],
    }
    return Request(scope)


class TestRequestValidator:
    BASE_URL = '/'

    def test_should_error_with_different_method_from_get(self) -> None:
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
            request = _build_request(
                f'{self.BASE_URL}?resource=people', method=method
            )
            with pytest.raises(MethodNotAllowedError) as exc_info:
                RequestValidator.validate(request)

            assert exc_info.value.status == HTTPStatus.METHOD_NOT_ALLOWED.value
            assert (
                exc_info.value.to_dict() == MethodNotAllowedError().to_dict()
            )

    def test_should_error_when_not_exist_resource(self) -> None:
        request = _build_request(
            f'{self.BASE_URL}?resource=nonexists', method='GET'
        )
        with pytest.raises(ValidationError) as exc_info:
            RequestValidator.validate(request)

        assert exc_info.value.error_count() == 1
        assert exc_info.value.errors()[0]['loc'] == ('resource',)
        assert exc_info.value.errors()[0]['type'] == 'literal_error'

    def test_should_error_when_not_passed_resource(self) -> None:
        request = _build_request(f'{self.BASE_URL}', method='GET')
        with pytest.raises(ValidationError) as exc_info:
            RequestValidator.validate(request)

        assert exc_info.value.error_count() == 1
        assert exc_info.value.errors()[0]['loc'] == ('resource',)
        assert exc_info.value.errors()[0]['type'] == 'missing'

    def test_should_error_when_page_is_not_int(self) -> None:
        request = _build_request(
            f'{self.BASE_URL}?resource=people&page=a', method='GET'
        )
        with pytest.raises(ValidationError) as exc_info:
            RequestValidator.validate(request)

        assert exc_info.value.error_count() == 1
        assert exc_info.value.errors()[0]['loc'] == ('page',)
        assert exc_info.value.errors()[0]['type'] == 'int_parsing'

    def test_should_error_when_id_is_not_int(self) -> None:
        request = _build_request(
            f'{self.BASE_URL}?resource=people&id=a', method='GET'
        )
        with pytest.raises(ValidationError) as exc_info:
            RequestValidator.validate(request)

        assert exc_info.value.error_count() == 1
        assert exc_info.value.errors()[0]['loc'] == ('id',)
        assert exc_info.value.errors()[0]['type'] == 'int_parsing'

    def test_should_error_when_use_id_and_search(self) -> None:
        request = _build_request(
            f'{self.BASE_URL}?resource=people&id=1&search=something',
            method='GET',
        )
        with pytest.raises(BadRequestError) as exc_info:
            RequestValidator.validate(request)

        assert exc_info.value.status == HTTPStatus.BAD_REQUEST.value
        assert exc_info.value.to_dict() == BadRequestError().to_dict()

    def test_should_error_when_use_id_and_page(self) -> None:
        request = _build_request(
            f'{self.BASE_URL}?resource=people&id=1&page=2',
            method='GET',
        )
        with pytest.raises(BadRequestError) as exc_info:
            RequestValidator.validate(request)

        assert exc_info.value.status == HTTPStatus.BAD_REQUEST.value
        assert exc_info.value.to_dict() == BadRequestError().to_dict()

    def test_validate_successful_resources_request(self) -> None:
        valid_resources = [
            'films',
            'people',
            'planets',
            'species',
            'starships',
            'vehicles',
        ]
        for resource in valid_resources:
            request = _build_request(
                f'{self.BASE_URL}?resource={resource}', method='GET'
            )
            RequestValidator.validate(request)

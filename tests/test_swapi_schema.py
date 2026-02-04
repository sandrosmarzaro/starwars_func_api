from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from schemas.swapi_query_params_schema import SwapiResource


class TestSwapiSchema:
    API_URL = '/api/v1/swapi/'

    def test_should_error_when_not_exist_resource(
        self, client: TestClient
    ) -> None:
        response = client.get(self.API_URL, params={'resource': 'nonexists'})

        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT.value
        assert response.json()['error'] == 'RequestValidationError'
        errors = response.json()['detail']
        assert len(errors) == 1
        assert errors[0]['loc'] == ['query', 'resource']
        assert errors[0]['type'] == 'enum'

    def test_should_error_when_not_passed_resource(
        self, client: TestClient
    ) -> None:
        response = client.get(self.API_URL)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT.value
        assert response.json()['error'] == 'RequestValidationError'
        errors = response.json()['detail']
        assert len(errors) == 1
        assert errors[0]['loc'] == ['query', 'resource']
        assert errors[0]['type'] == 'missing'

    def test_should_error_when_page_is_not_int(
        self, client: TestClient
    ) -> None:
        response = client.get(
            self.API_URL,
            params={'resource': 'people', 'page': 'a'},
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT.value
        assert response.json()['error'] == 'RequestValidationError'
        errors = response.json()['detail']
        assert any(
            error['loc'] == ['query', 'page']
            and error['type'] == 'int_parsing'
            for error in errors
        )

    def test_should_error_when_id_is_not_int(self, client: TestClient) -> None:
        response = client.get(
            self.API_URL,
            params={'resource': 'people', 'id': 'a'},
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT.value
        assert response.json()['error'] == 'RequestValidationError'
        errors = response.json()['detail']
        assert any(
            error['loc'] == ['query', 'id'] and error['type'] == 'int_parsing'
            for error in errors
        )

    def test_should_error_when_use_id_and_search(
        self, client: TestClient
    ) -> None:
        response = client.get(
            self.API_URL,
            params={'resource': 'people', 'id': 1, 'search': 'something'},
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT.value
        assert response.json()['error'] == 'RequestValidationError'

    def test_should_error_when_use_id_and_page(
        self, client: TestClient
    ) -> None:
        response = client.get(
            self.API_URL,
            params={'resource': 'people', 'id': 1, 'page': 2},
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT.value
        assert response.json()['error'] == 'RequestValidationError'

    @pytest.mark.usefixtures('mock_all_resources')
    def test_validate_successful_resources_request(
        self, client: TestClient
    ) -> None:
        for resource in SwapiResource:
            response = client.get(
                self.API_URL, params={'resource': resource.value}
            )
            assert response.status_code == HTTPStatus.OK.value

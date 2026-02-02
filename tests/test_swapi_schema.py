from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

API_URL = '/api/v1/swapi/'


class TestSwapiSchema:
    def test_should_error_when_not_exist_resource(
        self, client: TestClient
    ) -> None:
        response = client.get(f'{API_URL}?resource=nonexists')

        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT.value
        assert response.json()['error'] == 'RequestValidationError'
        errors = response.json()['detail']
        assert len(errors) == 1
        assert errors[0]['loc'] == ['query', 'resource']
        assert errors[0]['type'] == 'literal_error'

    def test_should_error_when_not_passed_resource(
        self, client: TestClient
    ) -> None:
        response = client.get(API_URL)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT.value
        assert response.json()['error'] == 'RequestValidationError'
        errors = response.json()['detail']
        assert len(errors) == 1
        assert errors[0]['loc'] == ['query', 'resource']
        assert errors[0]['type'] == 'missing'

    def test_should_error_when_page_is_not_int(
        self, client: TestClient
    ) -> None:
        response = client.get(f'{API_URL}?resource=people&page=a')

        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT.value
        assert response.json()['error'] == 'RequestValidationError'
        errors = response.json()['detail']
        assert any(
            error['loc'] == ['query', 'page']
            and error['type'] == 'int_parsing'
            for error in errors
        )

    def test_should_error_when_id_is_not_int(
        self, client: TestClient
    ) -> None:
        response = client.get(f'{API_URL}?resource=people&id=a')

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
            f'{API_URL}?resource=people&id=1&search=something'
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT.value
        assert response.json()['error'] == 'RequestValidationError'

    def test_should_error_when_use_id_and_page(
        self, client: TestClient
    ) -> None:
        response = client.get(f'{API_URL}?resource=people&id=1&page=2')

        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT.value
        assert response.json()['error'] == 'RequestValidationError'

    @pytest.mark.usefixtures('mock_all_resources')
    def test_validate_successful_resources_request(
        self, client: TestClient
    ) -> None:
        valid_resources = [
            'films',
            'people',
            'planets',
            'species',
            'starships',
            'vehicles',
        ]
        for resource in valid_resources:
            response = client.get(f'{API_URL}?resource={resource}')
            assert response.status_code == HTTPStatus.OK.value

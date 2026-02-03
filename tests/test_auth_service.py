from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


class TestAuthService:
    API_URL = '/api/v1/swapi/'

    @pytest.mark.usefixtures('mock_people_list')
    def test_should_return_unauthorized_when_api_key_header_missing(
        self, client_without_api_key: TestClient
    ) -> None:
        response = client_without_api_key.get(
            self.API_URL,
            params={'resource': 'people'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED.value
        assert response.json() == {
            'error': 'UnauthorizedError',
            'detail': 'X-API-Key header missing',
        }

    @pytest.mark.usefixtures('mock_people_list')
    def test_should_return_unauthorized_when_api_key_is_invalid(
        self, client_with_invalid_api_key: TestClient
    ) -> None:
        response = client_with_invalid_api_key.get(
            self.API_URL,
            params={'resource': 'people'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED.value
        assert response.json() == {
            'error': 'UnauthorizedError',
            'detail': 'Invalid API key',
        }

    @pytest.mark.usefixtures('mock_people_list')
    def test_should_allow_request_with_valid_api_key(
        self, client: TestClient
    ) -> None:
        response = client.get(self.API_URL, params={'resource': 'people'})

        assert response.status_code == HTTPStatus.OK.value

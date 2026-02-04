from http import HTTPStatus
from unittest.mock import patch

from fastapi.testclient import TestClient

from schemas.swapi_query_params_schema import SwapiResource


class TestRoot:
    API_URL = '/'

    def test_should_return_all_available_endpoints(
        self, client: TestClient
    ) -> None:
        mock_gateway_url = 'https://api.example.com'

        with patch(
            'api.v1.routers.root_router.settings.API_GATEWAY_URL',
            mock_gateway_url,
        ):
            response = client.get(self.API_URL)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        swapi_url = f'{mock_gateway_url}/api/v1/swapi?resource='

        assert data['documentation'] == f'{mock_gateway_url}/docs'
        for resource in SwapiResource:
            assert data[resource.value] == f'{swapi_url}{resource.value}'

    def test_should_return_correct_number_of_endpoints(
        self, client: TestClient
    ) -> None:
        response = client.get(self.API_URL)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        expected_count = len(SwapiResource) + 1  # resources + documentation
        assert len(data) == expected_count

    def test_documentation_should_be_first_key(
        self, client: TestClient
    ) -> None:
        response = client.get(self.API_URL)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        keys = list(data.keys())
        assert keys[0] == 'documentation'

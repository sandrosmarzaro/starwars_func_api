from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from tests.mock_data import (
    FILM_1,
    FILM_2,
    STARSHIP_12,
    TATOOINE,
    VEHICLE_14,
)


class TestSwapiDataExpand:
    API_URL = '/api/v1/swapi/'

    @pytest.mark.usefixtures('mock_person_with_expand')
    def test_should_expand_hateoas_links(self, client: TestClient) -> None:
        response = client.get(
            self.API_URL,
            params={'resource': 'people', 'id': 1, 'expand': True},
        )

        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert data['name'] == 'Luke Skywalker'
        assert data['homeworld'] == TATOOINE
        assert data['films'] == [FILM_1, FILM_2]
        assert data['vehicles'] == [VEHICLE_14]
        assert data['starships'] == [STARSHIP_12]
        assert data['url'] == 'https://swapi.dev/api/people/1/'

    @pytest.mark.usefixtures('mock_person_by_id')
    def test_should_not_expand_when_expand_is_false(
        self, client: TestClient
    ) -> None:
        response = client.get(
            self.API_URL,
            params={'resource': 'people', 'id': 1, 'expand': False},
        )

        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert data['homeworld'] == 'https://swapi.dev/api/planets/1/'

    @pytest.mark.usefixtures('mock_person_expand_with_error')
    def test_should_handle_expand_fetch_error_gracefully(
        self, client: TestClient
    ) -> None:
        response = client.get(
            self.API_URL,
            params={'resource': 'people', 'id': 1, 'expand': True},
        )

        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert data['homeworld']['error'] == 'Failed to fetch resource'

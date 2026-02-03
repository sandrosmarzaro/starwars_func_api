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
    def test_should_expand_all_hateoas_links(self, client: TestClient) -> None:
        response = client.get(
            self.API_URL,
            params={'resource': 'people', 'id': 1, 'expand': 'all'},
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
    def test_should_not_expand_when_expand_is_not_provided(
        self, client: TestClient
    ) -> None:
        response = client.get(
            self.API_URL,
            params={'resource': 'people', 'id': 1},
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
            params={'resource': 'people', 'id': 1, 'expand': 'all'},
        )

        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert data['homeworld']['error'] == 'Failed to fetch resource'

    @pytest.mark.usefixtures('mock_person_with_expand')
    def test_should_expand_only_specified_field(
        self, client: TestClient
    ) -> None:
        response = client.get(
            self.API_URL,
            params={'resource': 'people', 'id': 1, 'expand': 'homeworld'},
        )

        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert data['homeworld'] == TATOOINE
        assert data['films'] == [
            'https://swapi.dev/api/films/1/',
            'https://swapi.dev/api/films/2/',
        ]

    @pytest.mark.usefixtures('mock_person_with_expand')
    def test_should_expand_multiple_specified_fields(
        self, client: TestClient
    ) -> None:
        response = client.get(
            self.API_URL,
            params={
                'resource': 'people',
                'id': 1,
                'expand': 'homeworld,films',
            },
        )

        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert data['homeworld'] == TATOOINE
        assert data['films'] == [FILM_1, FILM_2]
        assert data['vehicles'] == ['https://swapi.dev/api/vehicles/14/']
        assert data['starships'] == ['https://swapi.dev/api/starships/12/']

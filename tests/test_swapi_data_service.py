from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from tests.mock_data import (
    ANAKIN_SKYWALKER,
    FILM_1,
    FILM_2,
    LUKE_SKYWALKER,
    STARSHIP_12,
    TATOOINE,
    VEHICLE_14,
)

API_URL = '/api/v1/swapi/'


class TestSwapiDataService:
    @pytest.mark.usefixtures('mock_people_list')
    def test_should_return_data_for_valid_resource(
        self, client: TestClient
    ) -> None:
        expected_data = {
            'count': 82,
            'next': 'https://swapi.dev/api/people/?page=2',
            'previous': None,
            'results': [LUKE_SKYWALKER, ANAKIN_SKYWALKER],
        }

        response = client.get(f'{API_URL}?resource=people')

        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == expected_data

    @pytest.mark.usefixtures('mock_person_by_id')
    def test_should_return_data_for_resource_with_id(
        self, client: TestClient
    ) -> None:
        response = client.get(f'{API_URL}?resource=people&id=1')

        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == LUKE_SKYWALKER

    @pytest.mark.usefixtures('mock_people_search')
    def test_should_return_data_with_search_param(
        self, client: TestClient
    ) -> None:
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [LUKE_SKYWALKER],
        }

        response = client.get(f'{API_URL}?resource=people&search=luke')

        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == expected_data

    @pytest.mark.usefixtures('mock_people_page')
    def test_should_return_data_with_page_param(
        self, client: TestClient
    ) -> None:
        expected_data = {
            'count': 82,
            'next': 'https://swapi.dev/api/people/?page=3',
            'previous': 'https://swapi.dev/api/people/?page=1',
            'results': [ANAKIN_SKYWALKER],
        }

        response = client.get(f'{API_URL}?resource=people&page=2')

        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == expected_data

    @pytest.mark.usefixtures('mock_not_found')
    def test_should_return_not_found_error_on_404(
        self, client: TestClient
    ) -> None:
        response = client.get(f'{API_URL}?resource=people&id=999')

        assert response.status_code == HTTPStatus.NOT_FOUND.value
        assert response.json() == {
            'error': 'NotFoundError',
            'detail': HTTPStatus.NOT_FOUND.description,
        }

    @pytest.mark.usefixtures('mock_bad_request')
    def test_should_return_bad_request_error_on_400(
        self, client: TestClient
    ) -> None:
        response = client.get(f'{API_URL}?resource=people')

        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        assert response.json() == {
            'error': 'BadRequestError',
            'detail': HTTPStatus.BAD_REQUEST.description,
        }

    @pytest.mark.usefixtures('mock_method_not_allowed')
    def test_should_return_method_not_allowed_error_on_405(
        self, client: TestClient
    ) -> None:
        response = client.get(f'{API_URL}?resource=people')

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED.value
        assert response.json() == {
            'error': 'MethodNotAllowedError',
            'detail': HTTPStatus.METHOD_NOT_ALLOWED.description,
        }

    @pytest.mark.usefixtures('mock_service_unavailable')
    def test_should_return_internal_server_error_on_unknown_status(
        self, client: TestClient
    ) -> None:
        response = client.get(f'{API_URL}?resource=people')

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value
        assert response.json() == {
            'error': 'InternalServerError',
            'detail': HTTPStatus.INTERNAL_SERVER_ERROR.description,
        }

    @pytest.mark.usefixtures('mock_person_with_expand')
    def test_should_expand_hateoas_links(self, client: TestClient) -> None:
        response = client.get(f'{API_URL}?resource=people&id=1&expand=true')

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
        response = client.get(f'{API_URL}?resource=people&id=1&expand=false')

        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert data['homeworld'] == 'https://swapi.dev/api/planets/1/'

    @pytest.mark.usefixtures('mock_person_expand_with_error')
    def test_should_handle_expand_fetch_error_gracefully(
        self, client: TestClient
    ) -> None:
        response = client.get(f'{API_URL}?resource=people&id=1&expand=true')

        assert response.status_code == HTTPStatus.OK.value
        data = response.json()
        assert data['homeworld']['error'] == 'Failed to fetch resource'

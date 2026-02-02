from http import HTTPStatus

import pytest
from httpx import AsyncClient

from exceptions.errors import (
    BadRequestError,
    InternalServerError,
    MethodNotAllowedError,
    NotFoundError,
)
from tests.conftest import ANAKIN_SKYWALKER, LUKE_SKYWALKER


class TestGetSwapiData:
    @pytest.mark.usefixtures('mock_people_list')
    async def test_should_return_data_for_valid_resource(
        self, client: AsyncClient
    ) -> None:
        expected_data = {
            'count': 82,
            'next': 'https://swapi.dev/api/people/?page=2',
            'previous': None,
            'results': [LUKE_SKYWALKER, ANAKIN_SKYWALKER],
        }

        response = await client.get('/?resource=people')

        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == expected_data

    @pytest.mark.usefixtures('mock_person_by_id')
    async def test_should_return_data_for_resource_with_id(
        self, client: AsyncClient
    ) -> None:
        response = await client.get('/?resource=people&id=1')

        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == LUKE_SKYWALKER

    @pytest.mark.usefixtures('mock_people_search')
    async def test_should_return_data_with_search_param(
        self, client: AsyncClient
    ) -> None:
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [LUKE_SKYWALKER],
        }

        response = await client.get('/?resource=people&search=luke')

        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == expected_data

    @pytest.mark.usefixtures('mock_people_page')
    async def test_should_return_data_with_page_param(
        self, client: AsyncClient
    ) -> None:
        expected_data = {
            'count': 82,
            'next': 'https://swapi.dev/api/people/?page=3',
            'previous': 'https://swapi.dev/api/people/?page=1',
            'results': [ANAKIN_SKYWALKER],
        }

        response = await client.get('/?resource=people&page=2')

        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == expected_data

    @pytest.mark.usefixtures('mock_not_found')
    async def test_should_return_not_found_error_on_404(
        self, client: AsyncClient
    ) -> None:
        response = await client.get('/?resource=people&id=999')

        assert response.status_code == HTTPStatus.NOT_FOUND.value
        assert response.json() == NotFoundError().to_dict()

    @pytest.mark.usefixtures('mock_bad_request')
    async def test_should_return_bad_request_error_on_400(
        self, client: AsyncClient
    ) -> None:
        response = await client.get('/?resource=people')

        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        assert response.json() == BadRequestError().to_dict()

    @pytest.mark.usefixtures('mock_method_not_allowed')
    async def test_should_return_method_not_allowed_error_on_405(
        self, client: AsyncClient
    ) -> None:
        response = await client.get('/?resource=people')

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED.value
        assert response.json() == MethodNotAllowedError().to_dict()

    @pytest.mark.usefixtures('mock_service_unavailable')
    async def test_should_return_internal_server_error_on_unknown_status(
        self, client: AsyncClient
    ) -> None:
        response = await client.get('/?resource=people')

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value
        assert response.json() == InternalServerError().to_dict()

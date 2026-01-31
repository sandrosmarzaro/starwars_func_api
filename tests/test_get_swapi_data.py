from http import HTTPStatus

import pytest
from flask import Flask

from exceptions.errors import (
    BadRequestError,
    InternalServerError,
    MethodNotAllowedError,
    NotFoundError,
)
from main import _get_swapi_data
from tests.conftest import ANAKIN_SKYWALKER, LUKE_SKYWALKER


class TestGetSwapiData:
    @pytest.mark.usefixtures('mock_people_list')
    def test_should_return_data_for_valid_resource(self, app: Flask) -> None:
        expected_data = {
            'count': 82,
            'next': 'https://swapi.dev/api/people/?page=2',
            'previous': None,
            'results': [LUKE_SKYWALKER, ANAKIN_SKYWALKER],
        }

        with app.app_context():
            response, status = _get_swapi_data({'resource': 'people'})

            assert status == HTTPStatus.OK.value
            assert response.json == expected_data

    @pytest.mark.usefixtures('mock_person_by_id')
    def test_should_return_data_for_resource_with_id(self, app: Flask) -> None:
        with app.app_context():
            response, status = _get_swapi_data(
                {'resource': 'people', 'id': '1'}
            )

            assert status == HTTPStatus.OK.value
            assert response.json == LUKE_SKYWALKER

    @pytest.mark.usefixtures('mock_people_search')
    def test_should_return_data_with_search_param(self, app: Flask) -> None:
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [LUKE_SKYWALKER],
        }

        with app.app_context():
            response, status = _get_swapi_data(
                {'resource': 'people', 'search': 'luke'}
            )

            assert status == HTTPStatus.OK.value
            assert response.json == expected_data

    @pytest.mark.usefixtures('mock_people_page')
    def test_should_return_data_with_page_param(self, app: Flask) -> None:
        expected_data = {
            'count': 82,
            'next': 'https://swapi.dev/api/people/?page=3',
            'previous': 'https://swapi.dev/api/people/?page=1',
            'results': [ANAKIN_SKYWALKER],
        }

        with app.app_context():
            response, status = _get_swapi_data(
                {'resource': 'people', 'page': '2'}
            )

            assert status == HTTPStatus.OK.value
            assert response.json == expected_data

    @pytest.mark.usefixtures('mock_not_found')
    def test_should_return_not_found_error_on_404(self, app: Flask) -> None:
        with app.app_context():
            response, status = _get_swapi_data(
                {'resource': 'people', 'id': '999'}
            )

            assert status == HTTPStatus.NOT_FOUND.value
            assert response.json == NotFoundError().to_dict()

    @pytest.mark.usefixtures('mock_bad_request')
    def test_should_return_bad_request_error_on_400(self, app: Flask) -> None:
        with app.app_context():
            response, status = _get_swapi_data({'resource': 'people'})

            assert status == HTTPStatus.BAD_REQUEST.value
            assert response.json == BadRequestError().to_dict()

    @pytest.mark.usefixtures('mock_method_not_allowed')
    def test_should_return_method_not_allowed_error_on_405(
        self, app: Flask
    ) -> None:
        with app.app_context():
            response, status = _get_swapi_data({'resource': 'people'})

            assert status == HTTPStatus.METHOD_NOT_ALLOWED.value
            assert response.json == MethodNotAllowedError().to_dict()

    @pytest.mark.usefixtures('mock_service_unavailable')
    def test_should_return_internal_server_error_on_unknown_status(
        self, app: Flask
    ) -> None:
        with app.app_context():
            response, status = _get_swapi_data({'resource': 'people'})

            assert status == HTTPStatus.INTERNAL_SERVER_ERROR.value
            assert response.json == InternalServerError().to_dict()

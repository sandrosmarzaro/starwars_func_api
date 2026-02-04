from collections.abc import Iterator
from http import HTTPStatus
from urllib.parse import urljoin

import httpx
import pytest
from fastapi.testclient import TestClient
from respx import MockRouter

from infra.settings import settings
from main import app
from tests.mock_data import (
    ANAKIN_SKYWALKER,
    ARVEL_CRYNYD,
    FILM_1,
    FILM_2,
    LUKE_SKYWALKER,
    STARSHIP_12,
    TATOOINE,
    VEHICLE_14,
    YODA,
)

BASE_URL = settings.SWAPI_BASE_URL


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_people_list(respx_mock: MockRouter) -> MockRouter:
    url = urljoin(BASE_URL, 'people/')
    data = {
        'count': 82,
        'next': 'https://swapi.dev/api/people/?page=2',
        'previous': None,
        'results': [LUKE_SKYWALKER, ANAKIN_SKYWALKER],
    }
    respx_mock.get(url).mock(
        return_value=httpx.Response(HTTPStatus.OK, json=data)
    )
    return respx_mock


@pytest.fixture
def mock_all_resources(respx_mock: MockRouter) -> MockRouter:
    resources = [
        'films',
        'people',
        'planets',
        'species',
        'starships',
        'vehicles',
    ]
    for resource in resources:
        url = urljoin(BASE_URL, f'{resource}/')
        data = {'count': 1, 'results': []}
        respx_mock.get(url).mock(
            return_value=httpx.Response(HTTPStatus.OK, json=data)
        )
    return respx_mock


@pytest.fixture
def mock_person_by_id(respx_mock: MockRouter) -> MockRouter:
    url = urljoin(urljoin(BASE_URL, 'people/'), '1')
    respx_mock.get(url).mock(
        return_value=httpx.Response(HTTPStatus.OK, json=LUKE_SKYWALKER)
    )
    return respx_mock


@pytest.fixture
def mock_people_search(respx_mock: MockRouter) -> MockRouter:
    url = urljoin(BASE_URL, 'people/')
    data = {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [LUKE_SKYWALKER],
    }
    respx_mock.get(url, params={'search': 'luke'}).mock(
        return_value=httpx.Response(HTTPStatus.OK, json=data)
    )
    return respx_mock


@pytest.fixture
def mock_people_page(respx_mock: MockRouter) -> MockRouter:
    url = urljoin(BASE_URL, 'people/')
    data = {
        'count': 82,
        'next': 'https://swapi.dev/api/people/?page=3',
        'previous': 'https://swapi.dev/api/people/?page=1',
        'results': [ANAKIN_SKYWALKER],
    }
    respx_mock.get(url, params={'page': '2'}).mock(
        return_value=httpx.Response(HTTPStatus.OK, json=data)
    )
    return respx_mock


@pytest.fixture
def mock_not_found(respx_mock: MockRouter) -> MockRouter:
    url = urljoin(urljoin(BASE_URL, 'people/'), '999')
    respx_mock.get(url).mock(return_value=httpx.Response(HTTPStatus.NOT_FOUND))
    return respx_mock


@pytest.fixture
def mock_bad_request(respx_mock: MockRouter) -> MockRouter:
    url = urljoin(BASE_URL, 'people/')
    respx_mock.get(url).mock(
        return_value=httpx.Response(HTTPStatus.BAD_REQUEST)
    )
    return respx_mock


@pytest.fixture
def mock_method_not_allowed(respx_mock: MockRouter) -> MockRouter:
    url = urljoin(BASE_URL, 'people/')
    respx_mock.get(url).mock(
        return_value=httpx.Response(HTTPStatus.METHOD_NOT_ALLOWED)
    )
    return respx_mock


@pytest.fixture
def mock_service_unavailable(respx_mock: MockRouter) -> MockRouter:
    url = urljoin(BASE_URL, 'people/')
    respx_mock.get(url).mock(
        return_value=httpx.Response(HTTPStatus.SERVICE_UNAVAILABLE)
    )
    return respx_mock


@pytest.fixture
def mock_person_with_expand(respx_mock: MockRouter) -> MockRouter:
    luke_simple = {
        'name': 'Luke Skywalker',
        'homeworld': 'https://swapi.dev/api/planets/1/',
        'films': [
            'https://swapi.dev/api/films/1/',
            'https://swapi.dev/api/films/2/',
        ],
        'species': [],
        'vehicles': ['https://swapi.dev/api/vehicles/14/'],
        'starships': ['https://swapi.dev/api/starships/12/'],
        'created': '2014-12-09T13:50:51.644000Z',
        'edited': '2014-12-20T21:17:56.891000Z',
        'url': 'https://swapi.dev/api/people/1/',
    }
    url = urljoin(urljoin(BASE_URL, 'people/'), '1')
    respx_mock.get(url).mock(
        return_value=httpx.Response(HTTPStatus.OK, json=luke_simple)
    )
    respx_mock.get('https://swapi.dev/api/planets/1/').mock(
        return_value=httpx.Response(HTTPStatus.OK, json=TATOOINE)
    )
    respx_mock.get('https://swapi.dev/api/films/1/').mock(
        return_value=httpx.Response(HTTPStatus.OK, json=FILM_1)
    )
    respx_mock.get('https://swapi.dev/api/films/2/').mock(
        return_value=httpx.Response(HTTPStatus.OK, json=FILM_2)
    )
    respx_mock.get('https://swapi.dev/api/vehicles/14/').mock(
        return_value=httpx.Response(HTTPStatus.OK, json=VEHICLE_14)
    )
    respx_mock.get('https://swapi.dev/api/starships/12/').mock(
        return_value=httpx.Response(HTTPStatus.OK, json=STARSHIP_12)
    )
    return respx_mock


@pytest.fixture
def mock_person_expand_with_error(respx_mock: MockRouter) -> MockRouter:
    luke_simple = {
        'name': 'Luke Skywalker',
        'homeworld': 'https://swapi.dev/api/planets/1/',
        'films': [],
        'species': [],
        'vehicles': [],
        'starships': [],
        'url': 'https://swapi.dev/api/people/1/',
    }
    url = urljoin(urljoin(BASE_URL, 'people/'), '1')
    respx_mock.get(url).mock(
        return_value=httpx.Response(HTTPStatus.OK, json=luke_simple)
    )
    respx_mock.get('https://swapi.dev/api/planets/1/').mock(
        return_value=httpx.Response(HTTPStatus.NOT_FOUND)
    )
    return respx_mock


@pytest.fixture
def mock_people_for_sort(respx_mock: MockRouter) -> MockRouter:
    url = urljoin(BASE_URL, 'people/')
    data = {
        'count': 4,
        'next': None,
        'previous': None,
        'results': [LUKE_SKYWALKER, ANAKIN_SKYWALKER, YODA, ARVEL_CRYNYD],
    }
    respx_mock.get(url).mock(
        return_value=httpx.Response(HTTPStatus.OK, json=data)
    )
    return respx_mock

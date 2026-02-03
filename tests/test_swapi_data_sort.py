from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


class TestSwapiDataSort:
    API_URL = '/api/v1/swapi/'
    @pytest.mark.usefixtures('mock_people_for_sort')
    def test_should_sort_by_name_ascending(self, client: TestClient) -> None:
        response = client.get(
            f'{self.API_URL}?resource=people&sort_by=name&sort_order=asc'
        )

        assert response.status_code == HTTPStatus.OK.value
        results = response.json()['results']
        names = [r['name'] for r in results]
        assert names == [
            'Anakin Skywalker',
            'Arvel Crynyd',
            'Luke Skywalker',
            'Yoda',
        ]

    @pytest.mark.usefixtures('mock_people_for_sort')
    def test_should_sort_by_name_descending(self, client: TestClient) -> None:
        response = client.get(
            f'{self.API_URL}?resource=people&sort_by=name&sort_order=desc'
        )

        assert response.status_code == HTTPStatus.OK.value
        results = response.json()['results']
        names = [r['name'] for r in results]
        assert names == [
            'Yoda',
            'Luke Skywalker',
            'Arvel Crynyd',
            'Anakin Skywalker',
        ]

    @pytest.mark.usefixtures('mock_people_for_sort')
    def test_should_sort_by_numeric_field_ascending(
        self, client: TestClient
    ) -> None:
        response = client.get(
            f'{self.API_URL}?resource=people&sort_by=height&sort_order=asc'
        )

        assert response.status_code == HTTPStatus.OK.value
        results = response.json()['results']
        heights = [r['height'] for r in results]
        assert heights == ['66', '172', '188', 'unknown']

    @pytest.mark.usefixtures('mock_people_for_sort')
    def test_should_sort_by_numeric_field_descending(
        self, client: TestClient
    ) -> None:
        response = client.get(
            f'{self.API_URL}?resource=people&sort_by=height&sort_order=desc'
        )

        assert response.status_code == HTTPStatus.OK.value
        results = response.json()['results']
        heights = [r['height'] for r in results]
        assert heights == ['188', '172', '66', 'unknown']

    @pytest.mark.usefixtures('mock_people_for_sort')
    def test_should_place_unknown_values_at_end(
        self, client: TestClient
    ) -> None:
        response = client.get(
            f'{self.API_URL}?resource=people&sort_by=mass&sort_order=asc'
        )

        assert response.status_code == HTTPStatus.OK.value
        results = response.json()['results']
        masses = [r['mass'] for r in results]
        assert masses[-1] == 'unknown'

    @pytest.mark.usefixtures('mock_people_for_sort')
    def test_should_default_to_ascending_order(
        self, client: TestClient
    ) -> None:
        response = client.get(f'{self.API_URL}?resource=people&sort_by=name')

        assert response.status_code == HTTPStatus.OK.value
        results = response.json()['results']
        names = [r['name'] for r in results]
        assert names == [
            'Anakin Skywalker',
            'Arvel Crynyd',
            'Luke Skywalker',
            'Yoda',
        ]

    @pytest.mark.usefixtures('mock_people_for_sort')
    def test_should_not_sort_when_sort_by_not_provided(
        self, client: TestClient
    ) -> None:
        response = client.get(f'{self.API_URL}?resource=people')

        assert response.status_code == HTTPStatus.OK.value
        results = response.json()['results']
        names = [r['name'] for r in results]
        assert names == [
            'Luke Skywalker',
            'Anakin Skywalker',
            'Yoda',
            'Arvel Crynyd',
        ]

    def test_should_error_when_sort_by_used_with_id(
        self, client: TestClient
    ) -> None:
        url = f'{self.API_URL}?resource=people&id=1&sort_by=name'
        response = client.get(url)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value
        errors = response.json()['detail']
        assert any('Cannot use sort_by with id' in str(e) for e in errors)

    def test_should_error_when_invalid_sort_order(
        self, client: TestClient
    ) -> None:
        response = client.get(
            f'{self.API_URL}?resource=people&sort_by=name&sort_order=invalid'
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value

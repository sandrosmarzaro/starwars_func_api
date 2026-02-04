import json

from fakeredis import FakeRedis

from repositories.cache_repository import CacheRepository
from schemas.swapi_query_params_schema import SwapiQueryParams, SwapiResource


class TestCacheKeyGeneration:
    def test_build_cache_key_list(
        self, cache_repository: CacheRepository
    ) -> None:
        params = SwapiQueryParams(resource=SwapiResource.PEOPLE)
        key = cache_repository.build_cache_key(params)
        assert key == 'swapi:v1:people:list:1:'

    def test_build_cache_key_with_id(
        self, cache_repository: CacheRepository
    ) -> None:
        params = SwapiQueryParams(resource=SwapiResource.PEOPLE, id=1)
        key = cache_repository.build_cache_key(params)
        assert key == 'swapi:v1:people:1:1:'

    def test_build_cache_key_with_page(
        self, cache_repository: CacheRepository
    ) -> None:
        params = SwapiQueryParams(resource=SwapiResource.PLANETS, page=3)
        key = cache_repository.build_cache_key(params)
        assert key == 'swapi:v1:planets:list:3:'

    def test_build_cache_key_with_search(
        self, cache_repository: CacheRepository
    ) -> None:
        params = SwapiQueryParams(resource=SwapiResource.FILMS, search='hope')
        key = cache_repository.build_cache_key(params)
        assert key == 'swapi:v1:films:list:1:hope'

    def test_build_cache_key_with_page_and_search(
        self, cache_repository: CacheRepository
    ) -> None:
        params = SwapiQueryParams(
            resource=SwapiResource.STARSHIPS, page=2, search='falcon'
        )
        key = cache_repository.build_cache_key(params)
        assert key == 'swapi:v1:starships:list:2:falcon'

    def test_cache_key_ignores_expand(
        self, cache_repository: CacheRepository
    ) -> None:
        params1 = SwapiQueryParams(resource=SwapiResource.PEOPLE, expand='all')
        params2 = SwapiQueryParams(
            resource=SwapiResource.PEOPLE, expand='homeworld'
        )
        params3 = SwapiQueryParams(resource=SwapiResource.PEOPLE)

        key1 = cache_repository.build_cache_key(params1)
        key2 = cache_repository.build_cache_key(params2)
        key3 = cache_repository.build_cache_key(params3)

        assert key1 == key2 == key3

    def test_cache_key_ignores_sort(
        self, cache_repository: CacheRepository
    ) -> None:
        params1 = SwapiQueryParams(
            resource=SwapiResource.PEOPLE, sort_by='name'
        )
        params2 = SwapiQueryParams(resource=SwapiResource.PEOPLE)

        key1 = cache_repository.build_cache_key(params1)
        key2 = cache_repository.build_cache_key(params2)

        assert key1 == key2


class TestCacheOperationsDisabled:
    def test_get_returns_none_when_disabled(
        self, cache_repository: CacheRepository
    ) -> None:
        cache_repository.enabled = False
        params = SwapiQueryParams(resource=SwapiResource.PEOPLE)

        result = cache_repository.get(params)

        assert result is None

    def test_set_returns_false_when_disabled(
        self, cache_repository: CacheRepository
    ) -> None:
        cache_repository.enabled = False
        params = SwapiQueryParams(resource=SwapiResource.PEOPLE)

        result = cache_repository.set(params, {'count': 1})

        assert result is False


class TestCacheOperationsEnabled:
    def test_set_and_get_data(self, cache_repository: CacheRepository) -> None:
        params = SwapiQueryParams(resource=SwapiResource.PEOPLE)
        data = {'count': 82, 'results': [{'name': 'Luke'}]}

        set_result = cache_repository.set(params, data)
        get_result = cache_repository.get(params)

        assert set_result is True
        assert get_result == data

    def test_get_returns_none_on_cache_miss(
        self, cache_repository: CacheRepository
    ) -> None:
        params = SwapiQueryParams(resource=SwapiResource.VEHICLES)

        result = cache_repository.get(params)

        assert result is None

    def test_different_params_have_different_cache(
        self, cache_repository: CacheRepository
    ) -> None:
        params1 = SwapiQueryParams(resource=SwapiResource.PEOPLE, page=1)
        params2 = SwapiQueryParams(resource=SwapiResource.PEOPLE, page=2)
        data1 = {'count': 82, 'page': 1}
        data2 = {'count': 82, 'page': 2}

        cache_repository.set(params1, data1)
        cache_repository.set(params2, data2)

        assert cache_repository.get(params1) == data1
        assert cache_repository.get(params2) == data2

    def test_same_params_different_expand_share_cache(
        self, cache_repository: CacheRepository
    ) -> None:
        params_no_expand = SwapiQueryParams(resource=SwapiResource.PEOPLE)
        params_with_expand = SwapiQueryParams(
            resource=SwapiResource.PEOPLE, expand='all'
        )
        data = {'count': 82, 'results': []}

        cache_repository.set(params_no_expand, data)
        result = cache_repository.get(params_with_expand)

        assert result == data

    def test_cache_stores_json_correctly(
        self, cache_repository: CacheRepository, redis_client: FakeRedis
    ) -> None:
        params = SwapiQueryParams(resource=SwapiResource.FILMS)
        data = {'count': 6, 'results': [{'title': 'A New Hope'}]}

        cache_repository.set(params, data)

        cache_key = cache_repository.build_cache_key(params)
        raw_value = redis_client.get(cache_key)
        assert raw_value is not None
        assert isinstance(raw_value, str)
        assert json.loads(raw_value) == data

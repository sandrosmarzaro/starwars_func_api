from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )
    SWAPI_BASE_URL: str = 'https://swapi.dev/api/'
    CLOUD_FUNC_URL: str = ''
    API_GATEWAY_URL: str = ''


@lru_cache
def _get_settings() -> _Settings:
    return _Settings()


settings = _get_settings()

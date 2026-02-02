from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )
    SWAPI_BASE_URL: str = 'https://swapi.dev/api/'
    API_KEY: str


@lru_cache
def _get_settings() -> _Settings:
    return _Settings()  # pyright: ignore[reportCallIssue]


settings = _get_settings()

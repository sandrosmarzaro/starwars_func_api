# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI wrapper around SWAPI (Star Wars API) with caching via Upstash Redis. Designed for deployment as a Google Cloud Function. Python 3.13+.

## Commands

All commands use [taskipy](https://github.com/taskipy/taskipy) (defined in `pyproject.toml`):

- `task run` - Start dev server (uvicorn on port 8080 with reload)
- `task test` - Run all tests with coverage
- `task lint` - Check linting (ruff)
- `task format` - Auto-fix lint errors then format (ruff)
- `task type` - Type check (pyright)
- `task commit` - Run all pre-commit hooks
- `task cover` - Show coverage report

Run a single test file: `pytest tests/test_cache_repository.py`
Run a single test: `pytest tests/test_cache_repository.py::test_function_name`

## Architecture

```
Request → FastAPI (main.py) → CORS middleware → Error handlers → Routers → Services → Repository/SWAPI
```

**Layers:**

- **Routers** (`api/v1/routers/`): HTTP endpoints. `root_router` serves `/`, `swapi_data_router` serves `/api/v1/swapi`.
- **Services** (`services/`): Business logic. `SwapiDataService` orchestrates the flow: check cache → fetch from SWAPI via httpx → optionally expand HATEOAS links (`ExpandSwapiDataService`) → optionally sort results (`SortSwapiDataService`) → cache response.
- **Repositories** (`repositories/`): `CacheRepository` abstracts Redis get/set with TTL-based keys.
- **Infrastructure** (`infra/`): `settings.py` (Pydantic Settings for env config), `redis_client.py` (Upstash Redis client factory, conditional on `CACHE_ENABLED`).
- **Schemas** (`schemas/`): Pydantic models for request validation (query params) and response serialization (per-resource types).
- **Exceptions** (`exceptions/`): Custom error classes inheriting `BaseError`, mapped to HTTP status codes via global handlers.

**Auth**: `X-API-Key` header extracted by `auth_service.py` (verification delegated to API Gateway).

## Testing

- **Async**: All tests run with `asyncio_mode = auto` (no need for `@pytest.mark.asyncio`)
- **HTTP mocking**: `respx` mocks httpx calls to SWAPI
- **Redis mocking**: `fakeredis.aioredis.FakeAsyncRedis` in fixtures (`tests/conftest.py`)
- **Test client**: FastAPI `TestClient` with dependency overrides for Redis
- **Sample data**: `tests/mock_data.py` contains SWAPI response fixtures

## Code Style

- **Ruff**: All rules enabled (`select = ['ALL']`), with specific ignores (docstrings `D`, `B008`, quotes `Q*`, assert `S101`, trailing comma `COM812`)
- **Line length**: 79 characters
- **Quote style**: Single quotes
- **Type checking**: Pyright strict mode
- **Imports**: `from __future__ import annotations` used throughout

## Environment Variables

See `.env.example`. Key variables: `SWAPI_BASE_URL`, `CACHE_ENABLED`, `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`, `CACHE_TTL_SECONDS` (default 86400).

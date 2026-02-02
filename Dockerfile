FROM python:3.13-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:0.8.21 /uv /uvx /bin/

RUN apk add gcc musl-dev --no-cache

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev
COPY . /app
RUN uv sync --frozen --no-dev

FROM python:3.13-alpine AS production

COPY --from=ghcr.io/astral-sh/uv:0.8.21 /uv /uvx /bin/

RUN apk add libpq --no-cache

RUN addgroup -S nonroot && adduser -S -G nonroot nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER nonroot

WORKDIR /app

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


from http import HTTPStatus

from starlette.responses import JSONResponse, Response

from exceptions.errors import BaseError
from utils.cors import build_cors_headers, build_cors_options_headers


def api_response(
    data: dict,
    status: int = HTTPStatus.OK.value,
    headers: dict[str, str] | None = None,
) -> Response:
    return JSONResponse(
        content=data,
        status_code=status,
        headers=headers or build_cors_headers(),
    )


def error_response(error: BaseError) -> Response:
    return api_response(error.to_dict(), error.status)


def cors_preflight_response() -> Response:
    return Response(
        status_code=HTTPStatus.NO_CONTENT.value,
        headers=build_cors_options_headers(),
    )

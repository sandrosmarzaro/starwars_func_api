from http import HTTPStatus

from flask import jsonify

from exceptions.errors import BaseError
from models.api_response import ApiResponse
from utils.cors import build_cors_headers, build_cors_options_headers


def api_response(
    data: dict,
    status: int = HTTPStatus.OK.value,
    headers: dict[str, str] | None = None,
) -> ApiResponse:
    return ApiResponse(
        jsonify(data),
        status,
        headers or build_cors_headers(),
    )


def error_response(error: BaseError) -> ApiResponse:
    return api_response(error.to_dict(), error.status)


def cors_preflight_response() -> ApiResponse:
    return ApiResponse(
        jsonify({}),
        HTTPStatus.NO_CONTENT.value,
        build_cors_options_headers(),
    )

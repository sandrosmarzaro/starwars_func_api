from typing import NamedTuple

from flask import Response


class ApiResponse(NamedTuple):
    body: Response
    status: int
    headers: dict[str, str]

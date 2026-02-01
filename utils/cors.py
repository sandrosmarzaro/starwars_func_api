def build_cors_headers() -> dict[str, str]:
    return {'Access-Control-Allow-Origin': '*'}


def build_cors_options_headers() -> dict[str, str]:
    headers = build_cors_headers()
    headers.update(
        {
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
        }
    )

    return headers

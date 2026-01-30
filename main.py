import functions_framework
from flask import Request


@functions_framework.http
def starwars_func(request: Request) -> tuple:
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
        }
        return ('', 204, headers)

    headers = {'Access-Control-Allow-Origin': '*'}

    return ('Hello World!', 200, headers)

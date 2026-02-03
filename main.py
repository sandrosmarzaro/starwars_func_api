from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routers.swapi_data_router import router as swapi_router
from exceptions.error_handler import add_exceptions_handler

openapi_tags = [
    {
        'name': 'swapi',
        'description': 'Operations to query Star Wars API (SWAPI) resources',
        'externalDocs': {
            'description': 'SWAPI Documentation',
            'url': 'https://swapi.dev/documentation',
        },
    },
]

app = FastAPI(
    title='Star Wars Wrap API',
    summary='A wrapper API for SWAPI (Star Wars API)',
    description='This API proxies requests to SWAPI with validation '
    'and provides access to Star Wars universe data including '
    'people, planets, starships, films, species, and vehicles.',
    version='1.0.0',
    contact={
        'name': 'Sandro Smarzaro',
        'email': 'sansmarzaro@gmail.com',
        'url': 'https://www.linkedin.com/in/sandrosmarzaro/',
    },
    license_info={
        'name': 'The MIT License',
        'identifier': 'MIT',
        'url': 'https://opensource.org/license/mit',
    },
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'OPTIONS'],
    allow_headers=['Content-Type', 'X-API-Key'],
    max_age=3600,
)

add_exceptions_handler(app)

app.include_router(swapi_router, prefix='/api/v1')

from fastapi import APIRouter

from infra.settings import settings

router = APIRouter(tags=['root'])

RESOURCES = ['films', 'people', 'planets', 'species', 'starships', 'vehicles']


@router.get(
    '/',
    summary='API Root',
    description='Lists all available API resources and endpoints.',
    response_description='Available API endpoints',
)
async def get_root() -> dict[str, str]:
    base_url = settings.API_GATEWAY_URL.rstrip('/')
    swapi_url = f'{base_url}/api/v1/swapi?resource='
    return {
        'documentation': f'{base_url}/docs',
        **{resource: f'{swapi_url}{resource}' for resource in RESOURCES},
    }

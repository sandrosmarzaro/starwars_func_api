from fastapi import APIRouter, Depends

from infra.settings import settings
from schemas.swapi_query_params_schema import SwapiResource
from services.auth_service import verify_api_key

router = APIRouter(tags=['root'], dependencies=[Depends(verify_api_key)])


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
        **{r.value: f'{swapi_url}{r.value}' for r in SwapiResource},
    }

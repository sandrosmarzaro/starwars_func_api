from typing import Annotated

from pydantic import BaseModel, Field

from schemas.swapi_query_params_schema import SwapiResource

UrlField = Annotated[str, Field(json_schema_extra={'format': 'uri'})]


class RootResponse(BaseModel):
    """API root response with available endpoints and resources."""

    documentation: UrlField = Field(
        description='URL to the API documentation (Swagger UI)'
    )
    films: UrlField = Field(description='URL to query Star Wars films')
    people: UrlField = Field(description='URL to query Star Wars characters')
    planets: UrlField = Field(description='URL to query Star Wars planets')
    species: UrlField = Field(description='URL to query Star Wars species')
    starships: UrlField = Field(description='URL to query Star Wars starships')
    vehicles: UrlField = Field(description='URL to query Star Wars vehicles')

    model_config = {
        'json_schema_extra': {
            'example': {
                'documentation': 'https://api.example.com/docs',
                **{
                    r.value: f'https://api.example.com/api/v1/swapi?resource={r.value}'
                    for r in SwapiResource
                },
            }
        }
    }

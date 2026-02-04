from enum import Enum

from pydantic import BaseModel, Field, PositiveInt, model_validator


class SwapiResource(str, Enum):
    FILMS = 'films'
    PEOPLE = 'people'
    PLANETS = 'planets'
    SPECIES = 'species'
    STARSHIPS = 'starships'
    VEHICLES = 'vehicles'


class SortOrder(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class SwapiQueryParams(BaseModel):
    resource: SwapiResource = Field(
        description='The Star Wars resource type to query',
        examples=['people', 'planets', 'films'],
    )
    id: PositiveInt | None = Field(
        default=None,
        description='Unique identifier to retrieve a specific resource',
        examples=[1, 2, 3],
    )
    page: PositiveInt | None = Field(
        default=None,
        description='Page number for paginated results',
        examples=[1, 2, 3],
    )
    search: str | None = Field(
        default=None,
        description='Search term to filter results by name or title',
        examples=['skywalker', 'jedi'],
    )
    expand: str | None = Field(
        default=None,
        description='Expand HATEOAS links. Use "all" to expand all fields, '
        'or specify field names separated by comma (e.g., "homeworld,films")',
        examples=['all', 'homeworld', 'homeworld,films'],
    )
    sort_by: str | None = Field(
        default=None,
        description='Field name to sort results by',
        examples=['name', 'created', 'height'],
    )
    sort_order: SortOrder = Field(
        default=SortOrder.ASC,
        description='Sort order: asc (ascending) or desc (descending)',
    )

    @model_validator(mode='after')
    def validate_query_combations(self) -> 'SwapiQueryParams':
        if self.id and (self.page or self.search or self.sort_by):
            msg = 'Cannot use id with page, search and sort'
            raise ValueError(msg)
        return self

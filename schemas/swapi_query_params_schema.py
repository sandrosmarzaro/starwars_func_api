from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, PositiveInt, model_validator


class SortOrder(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class SwapiQueryParams(BaseModel):
    resource: Literal[
        'films', 'people', 'planets', 'species', 'starships', 'vehicles'
    ] = Field(examples=['people', 'planets', 'films'])
    id: PositiveInt | None = Field(default=None, examples=[1, 2, 3])
    page: PositiveInt | None = Field(default=None, examples=[1, 2, 3])
    search: str | None = Field(default=None, examples=['skywalker', 'jedi'])
    expand: bool = Field(
        default=False,
        description='Expand first-level HATEOAS links with actual data',
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
        if self.id and (self.page or self.search):
            msg = 'Cannot use id with page or search'
            raise ValueError(msg)
        if self.id and self.sort_by:
            msg = 'Cannot use sort_by with id (single resource)'
            raise ValueError(msg)
        return self

from typing import Literal

from pydantic import BaseModel, Field, PositiveInt, model_validator


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

    @model_validator(mode='after')
    def validate_query_combations(self) -> 'SwapiQueryParams':
        if self.id and (self.page or self.search):
            msg = 'Cannot use id with page or search'
            raise ValueError(msg)
        return self

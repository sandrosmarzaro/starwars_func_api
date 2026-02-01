from typing import Literal

from pydantic import BaseModel, PositiveInt, model_validator

from exceptions.errors import BadRequestError


class SwapiQueryParams(BaseModel):
    resource: Literal[
        'films', 'people', 'planets', 'species', 'starships', 'vehicles'
    ]
    id: PositiveInt | None = None
    page: PositiveInt | None = None
    search: str | None = None

    @model_validator(mode='after')
    def validate_query_combations(self) -> 'SwapiQueryParams':
        if self.id and (self.page or self.search):
            raise BadRequestError
        return self

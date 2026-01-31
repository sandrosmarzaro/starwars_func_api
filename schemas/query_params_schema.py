from pydantic import BaseModel, NonNegativeInt


class SwapiQueryParams(BaseModel):
    id: NonNegativeInt | None = None
    page: NonNegativeInt | None = None
    search: str | None = None

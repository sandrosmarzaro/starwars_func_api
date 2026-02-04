from pydantic import BaseModel, Field


class PersonResponse(BaseModel):
    name: str = Field(description='The name of this person')
    height: str = Field(description='Height in centimeters')
    mass: str = Field(description='Mass in kilograms')
    hair_color: str = Field(description='Hair color')
    skin_color: str = Field(description='Skin color')
    eye_color: str = Field(description='Eye color')
    birth_year: str = Field(description='Birth year (BBY/ABY)')
    gender: str = Field(description='Gender')
    homeworld: str = Field(description='URL of the homeworld planet')
    films: list[str] = Field(description='URLs of films appeared in')
    species: list[str] = Field(description='URLs of species')
    vehicles: list[str] = Field(description='URLs of vehicles piloted')
    starships: list[str] = Field(description='URLs of starships piloted')
    url: str = Field(description='URL of this resource')


class FilmResponse(BaseModel):
    title: str = Field(description='Title of this film')
    episode_id: int = Field(description='Episode number')
    opening_crawl: str = Field(description='Opening paragraphs')
    director: str = Field(description='Director name')
    producer: str = Field(description='Producer name(s)')
    release_date: str = Field(description='ISO 8601 release date')
    characters: list[str] = Field(description='URLs of characters')
    planets: list[str] = Field(description='URLs of planets')
    starships: list[str] = Field(description='URLs of starships')
    vehicles: list[str] = Field(description='URLs of vehicles')
    species: list[str] = Field(description='URLs of species')
    url: str = Field(description='URL of this resource')


class PlanetResponse(BaseModel):
    name: str = Field(description='Name of this planet')
    rotation_period: str = Field(description='Rotation period in hours')
    orbital_period: str = Field(description='Orbital period in days')
    diameter: str = Field(description='Diameter in kilometers')
    climate: str = Field(description='Climate')
    gravity: str = Field(description='Gravity')
    terrain: str = Field(description='Terrain')
    surface_water: str = Field(description='Percentage of water surface')
    population: str = Field(description='Average population')
    residents: list[str] = Field(description='URLs of residents')
    films: list[str] = Field(description='URLs of films appeared in')
    url: str = Field(description='URL of this resource')


class SpeciesResponse(BaseModel):
    name: str = Field(description='Name of this species')
    classification: str = Field(description='Classification')
    designation: str = Field(description='Designation')
    average_height: str = Field(description='Average height in cm')
    skin_colors: str = Field(description='Common skin colors')
    hair_colors: str = Field(description='Common hair colors')
    eye_colors: str = Field(description='Common eye colors')
    average_lifespan: str = Field(description='Average lifespan in years')
    homeworld: str | None = Field(description='URL of homeworld planet')
    language: str = Field(description='Common language')
    people: list[str] = Field(description='URLs of people')
    films: list[str] = Field(description='URLs of films appeared in')
    url: str = Field(description='URL of this resource')


class StarshipResponse(BaseModel):
    name: str = Field(description='Name of this starship')
    model: str = Field(description='Model or official name')
    manufacturer: str = Field(description='Manufacturer')
    cost_in_credits: str = Field(description='Cost new in credits')
    length: str = Field(description='Length in meters')
    max_atmosphering_speed: str = Field(description='Max atmospheric speed')
    crew: str = Field(description='Personnel needed to run')
    passengers: str = Field(description='Number of passengers')
    cargo_capacity: str = Field(description='Max cargo in kilograms')
    consumables: str = Field(description='Max consumables duration')
    hyperdrive_rating: str = Field(description='Hyperdrive class')
    MGLT: str = Field(description='Megalights per hour')
    starship_class: str = Field(description='Starship class')
    pilots: list[str] = Field(description='URLs of pilots')
    films: list[str] = Field(description='URLs of films appeared in')
    url: str = Field(description='URL of this resource')


class VehicleResponse(BaseModel):
    name: str = Field(description='Name of this vehicle')
    model: str = Field(description='Model or official name')
    manufacturer: str = Field(description='Manufacturer')
    cost_in_credits: str = Field(description='Cost new in credits')
    length: str = Field(description='Length in meters')
    max_atmosphering_speed: str = Field(description='Max atmospheric speed')
    crew: str = Field(description='Personnel needed to run')
    passengers: str = Field(description='Number of passengers')
    cargo_capacity: str = Field(description='Max cargo in kilograms')
    consumables: str = Field(description='Max consumables duration')
    vehicle_class: str = Field(description='Vehicle class')
    pilots: list[str] = Field(description='URLs of pilots')
    films: list[str] = Field(description='URLs of films appeared in')
    url: str = Field(description='URL of this resource')


SingleResourceResponse = (
    PersonResponse
    | FilmResponse
    | PlanetResponse
    | SpeciesResponse
    | StarshipResponse
    | VehicleResponse
)


class PaginatedResponse(BaseModel):
    count: int = Field(description='Total number of resources')
    next: str | None = Field(description='URL to the next page')
    previous: str | None = Field(description='URL to the previous page')
    results: list[SingleResourceResponse] = Field(description='Resources')


SwapiResponse = SingleResourceResponse | PaginatedResponse

from fastapi.openapi.models import Example

SWAPI_EXAMPLES: dict[str, Example] = {
    'list_people': {
        'summary': 'List people',
        'description': 'Get all Star Wars characters',
        'value': {'resource': 'people'},
    },
    'get_person': {
        'summary': 'Get person by ID',
        'description': 'Get Luke Skywalker by ID',
        'value': {'resource': 'people', 'id': 1},
    },
    'search_people': {
        'summary': 'Search people',
        'description': 'Search for Skywalker characters',
        'value': {'resource': 'people', 'search': 'skywalker'},
    },
    'list_planets': {
        'summary': 'List planets with pagination',
        'description': 'Get second page of planets',
        'value': {'resource': 'planets', 'page': 2},
    },
    'list_films': {
        'summary': 'List films',
        'description': 'Get all Star Wars films',
        'value': {'resource': 'films'},
    },
}

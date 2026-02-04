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
    'expand_all': {
        'summary': 'Expand all HATEOAS links',
        'description': 'Get person with all related resources expanded',
        'value': {'resource': 'people', 'id': 1, 'expand': 'all'},
    },
    'expand_specific': {
        'summary': 'Expand specific fields',
        'description': 'Get person with homeworld and films expanded',
        'value': {'resource': 'people', 'id': 1, 'expand': 'homeworld,films'},
    },
    'sort_asc': {
        'summary': 'Sort ascending',
        'description': 'Get people sorted by name ascending',
        'value': {'resource': 'people', 'sort_by': 'name'},
    },
    'sort_desc': {
        'summary': 'Sort descending',
        'description': 'Get people sorted by height descending',
        'value': {
            'resource': 'people',
            'sort_by': 'height',
            'sort_order': 'desc',
        },
    },
    'list_films': {
        'summary': 'List films',
        'description': 'Get all Star Wars films',
        'value': {'resource': 'films'},
    },
}

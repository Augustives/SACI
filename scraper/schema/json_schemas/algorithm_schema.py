algorithm_schema = {
    'title': 'Algorithm',
    'description': 'An extracted algorithm with its atributes',
    'properties': {
        'name': {
            'description': 'The name of the algorithm',
            'type': 'string'
        },
        'time_complexity': {
            'description': 'The time complexity of the algorithm',
            'type': 'string'
        },
        # space_complexity
        'raw_algorithm': {
            'description': 'The algorithm code',
            'type': 'string'
        }
    },
    'required': []
}

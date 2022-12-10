algorithm_schema = {
    "title": "Algorithm",
    "description": "An extracted algorithm with its atributes",
    "type": "object",
    "properties": {
        "name": {"description": "The name of the algorithm", "type": "string"},
        "time_complexity": {
            "description": "The time complexity of the algorithm",
            "type": ["string", "null"],
        },
        "space_complexity": {
            "description": "The space complexity of the algorithm",
            "type": ["string", "null"],
        },
        "url": {"description": "The URL of the given algorithm", "type": "string"},
        "algorithm": {
            "description": "The algorithm code",
            "type": "object",
            "properties": {"code": {"type": "string"}, "comments": {"type": "string"}},
        },
    },
}

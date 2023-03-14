scraper_output = {
    "title": "Scraper Output",
    "description": "An extracted algorithm with its atributes",
    "type": "object",
    "properties": {
        "name": {
            "description": "The name of the algorithm",
            "type": ["string", "null"],
        },
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
            "description": "The algorithm implementations",
            "type": "object",
            "properties": {
                "code": {"description": "The code of the algorithm", "type": "string"},
                "comments": {
                    "description": "The first few comments in the code",
                    "type": "string",
                },
            },
        },
    },
}

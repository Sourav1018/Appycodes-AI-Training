calculator_tool = {
    "type": "function",
    "name": "evaluate_expression",
    "description": "Evaluate a math expression (supports add, subtract, multiply, divide, sqrt, log, pow, etc.)",
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The math expression, e.g. 'sqrt(16) + 10'",
            }
        },
        "required": ["expression"],
    },
}

weather_tool = {
    "type": "function",
    "name": "get_weather",
    "description": "Get the current weather for a given location, place, or city",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name and optional country code, e.g., 'London, UK'",
            }
        },
        "required": ["location"],
    },
}

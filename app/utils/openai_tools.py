# app/utils/openai_tools.py
calculator_tool = {
    "type": "function",   # optional, but recommended
    "name": "evaluate_expression",
    "description": "Evaluate a math expression (supports add, subtract, multiply, divide, sqrt, log, pow, etc.)",
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The math expression, e.g. 'sqrt(16) + 10'"
            }
        },
        "required": ["expression"]
    }
}

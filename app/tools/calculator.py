import math

allowed = {
    "sqrt": math.sqrt,
    "pow": math.pow,
    "log": math.log,
    "log10": math.log10,
    "abs": abs,
    "pi": math.pi,
    "e": math.e,
}

def evaluate_expression(expression: str) -> str:
    try:
        return str(eval(expression, {"__builtins__": {}}, allowed))
    except Exception as e:
        return f"Error: {str(e)}"

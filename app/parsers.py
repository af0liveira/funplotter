import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

# Define 'x' as the only variable allowed
x = sp.symbols('x')
ALLOWED_VARIABLES = {'x': x}

# Dictionary of all functions understood by 'sympy'
ALLOWED_FUNCTIONS = {name.lower(): func
                     for name, func in vars(sp.functions).items()
                     if callable(func)}
ALLOWED_FUNCTIONS.update(
    {
        'diff': sp.diff,
        'integrate': sp.integrate,
    }
)

# Functions allowed when using 'parse_expr'
GLOBAL_REFERENCES = {
    'Integer': sp.Integer,
    'Float': sp.Float,
    'pi': sp.pi,
}


class ParsingError(Exception):

    def __init__(self, message=None):
        if not message:
            message = ("Input could not be parsed!"
                       " Make sure you entered valid expressions.")
        self.message = message
        super().__init__(self.message)


def sanitize_numeric_input(raw_input: str) -> float:
    """Parse string into numerical values."""
    try:
        sanitized_value = float(parse_expr(raw_input.lower(),
                                           local_dict=ALLOWED_FUNCTIONS,
                                           global_dict=GLOBAL_REFERENCES))
    except Exception:
        raise ParsingError()

    return sanitized_value


def sanitize_function_input(raw_input: str) -> float:
    """Parse string representing the mathematical function."""
    local_dict = {'x': x, **ALLOWED_FUNCTIONS}

    try:
        sanitized_value = parse_expr(raw_input.lower(), local_dict=local_dict,
                                     global_dict=GLOBAL_REFERENCES)
    except Exception:
        raise ParsingError()

    return sanitized_value


def parse_function(f_expr: str, x_min: str | float, x_max: str | float) -> dict:
    NUM_POINTS = 1000

    # Define the grid of 'x' values
    x_start = sanitize_numeric_input(x_min)
    x_stop = sanitize_numeric_input(x_max)
    x_values = np.linspace(x_start, x_stop, num=NUM_POINTS, endpoint=True)

    # Create a lambda function from 'f(x)'
    sp_expr = sanitize_function_input(f_expr)
    f = sp.lambdify(x, sp_expr, 'numpy')

    # Generate the grid of 'y' values
    # Note that constant functions return a single value by default!
    if sp_expr.is_constant():
        y_values = np.full_like(x_values, f(x_values), dtype=float)
    else:
        y_values = f(x_values)

    function = {
        'label': f"{sp_expr}",
        'x_min': f"{x_start:.2f}",
        'x_max': f"{x_stop:.2f}",
        'data': [{'x': x, 'y': y} for x, y in zip(x_values, y_values)],
    }

    return function

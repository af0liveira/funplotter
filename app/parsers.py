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
            message = ("Invalid expression!")
        self.message = message
        super().__init__(self.message)


def parse_function_form(form):
    fx_str, fx = _parse_function_field(form.function)
    x_min = _parse_numeric_field(form.xMin)
    x_max = _parse_numeric_field(form.xMax)

    if x_min and x_max and x_max <= x_min:
        msg = "Upper limit must be greater than lower limit."
        form.xMax.errors.append(msg)

    if form.function.errors or form.xMin.errors or form.xMax.errors:
        raise ParsingError()

    return _parse_plot_data(fx_str, fx, x_min, x_max)


def _parse_function_field(form_field):
    """Convert string into a simpy FunctionClass instance."""
    local_dict = {'x': x, **ALLOWED_FUNCTIONS}

    try:
        sanitized_expr = parse_expr(form_field.data.lower(),
                                    local_dict=local_dict,
                                    global_dict=GLOBAL_REFERENCES)
        fx = sp.lambdify(x, sanitized_expr, 'numpy')
    except Exception:
        msg = "Input is not a valid univariate function of x."
        form_field.errors.append(msg)
    else:
        return sanitized_expr, fx

    return None, None


def _parse_numeric_field(form_field):
    """Convert string into the corresponding float value."""
    try:
        num_value = float(
            parse_expr(form_field.data.lower(), local_dict=ALLOWED_FUNCTIONS,
                       global_dict=GLOBAL_REFERENCES)
        )
    except Exception:
        msg = "Input does not corresppond to a unique value."
        form_field.errors.append(msg)
    else:
        return num_value


def _parse_plot_data(fx_str, fx, x_min, x_max):
    """Generate data for plotting function."""
    NUM_POINTS = 1000   # Grid density

    # Define the grid of 'x' values
    x_values = np.linspace(x_min, x_max, num=NUM_POINTS, endpoint=True)

    plot_data = {
        'label': f"{fx_str}",
        'x_min': f"{x_min:.2f}",
        'x_max': f"{x_max:.2f}",
        'data': [{'x': x, 'y': fx(x)} for x in x_values],
    }

    return plot_data

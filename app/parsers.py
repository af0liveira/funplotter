import numpy as np
import sympy as sp


def parse_function(f_expr: str, x_min: float, x_max: float) -> dict:
    # X_STEP = 1e-2
    NUM_POINTS = 1000

    x = sp.symbols('x')
    sp_expr = sp.sympify(f_expr)
    f = sp.lambdify(x, sp_expr, 'numpy')

    x_values = np.linspace(x_min, x_max, num=NUM_POINTS, endpoint=True)
    # x_values = np.arange(x_min, x_max+X_STEP, step=X_STEP)

    if sp_expr.is_constant():
        y_values = np.full_like(x_values, float(sp_expr), dtype=float)
    else:
        y_values = f(x_values)

    function = {
        'label': f_expr,
        'x_min': x_min,
        'x_max': x_max,
        'data': [{'x': x, 'y': y} for x, y in zip(x_values, y_values)],
    }

    return function

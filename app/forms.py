import sympy as sp

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField 
from wtforms.validators import DataRequired, ValidationError
from markupsafe import Markup


def validate_function_expression(form, field):
    """Ensure that the expression represents an explicit function of 'x'."""
    try:
        free_symbols = sp.sympify(field.data).free_symbols
        assert free_symbols <= {sp.symbols('x')}
    except Exception as e:
        raise ValidationError("Invalid function expression.")


def validate_value(form, field):
    """Ensure that the input expression represents a real number."""
    try:
        value = float(sp.sympify(field.data))
    except Exception as e:
        raise ValidationError("Invalid value.")


class FunctionForm(FlaskForm):
    """Base class for function form classes."""
    function = StringField(
        Markup("f(x) ="),
        validators = [
            DataRequired(),
            validate_function_expression,
        ],
    )
    xMin = StringField(
        Markup("x<sub>min</sub> ="),
        validators = [
            DataRequired(),
            validate_value,
        ],
    )
    xMax = StringField(
        Markup("x<sub>max</sub> ="),
        validators = [
            DataRequired(),
            validate_value,
        ],
    )


class AddFunctionForm(FunctionForm):
    """Form for adding new function."""
    submit = SubmitField("Add Function")


class EditFunctionForm(FunctionForm):
    """Form for updating existing function."""
    update = SubmitField('Update')
    delete = SubmitField('Delete')


def create_form(form_type, **kwargs):
    """Create the requested form type."""
    match form_type.lower():
        case 'new_function':
            return AddFunctionForm(**kwargs)
        case 'function_update':
            return EditFunctionForm(**kwargs)
        case _:
            raise ValueError(f"Unknown form type: {form_type}")

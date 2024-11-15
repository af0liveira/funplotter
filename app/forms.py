from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, ValidationError
from markupsafe import Markup


def validate_input(form, field):
    """Restrict input to alphanumeric characters and basic math symbols."""
    ALLOWED_SYMBOLS = '+-*/^()., '

    if not all(char.isalnum() or char in ALLOWED_SYMBOLS for char in
               field.data):
        raise ValidationError("Invalid characters in expression")


class FunctionForm(FlaskForm):
    """Base class for function form classes."""
    function = StringField(
        Markup("f(x):"),
        validators=[
            DataRequired(),
            validate_input,
        ],
    )
    xMin = StringField(
        Markup("x<sub>min</sub>:"),
        validators=[
            DataRequired(),
            validate_input,
        ],
    )
    xMax = StringField(
        Markup("x<sub>max</sub>:"),
        validators=[
            DataRequired(),
            validate_input,
        ],
    )


class PlotFunctionForm(FunctionForm):
    """Form for adding new function."""
    submit = SubmitField("Plot Function")


class EditFunctionForm(FunctionForm):
    """Form for updating existing function."""
    update = SubmitField('Update')
    delete = SubmitField('Delete')


def create_form(form_type, **kwargs):
    """Create the requested form type."""
    match form_type.lower():
        case 'new_function':
            return PlotFunctionForm(**kwargs)
        case 'function_update':
            return EditFunctionForm(**kwargs)
        case _:
            raise ValueError(f"Unknown form type: {form_type}")

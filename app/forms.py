import sympy as sp

from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField 
from wtforms.validators import DataRequired, Regexp, ValidationError
from markupsafe import Markup


class AddFunctionForm(FlaskForm):
    function = StringField(
        Markup("f(x) ="),
        validators=[
            DataRequired(),
            Regexp(r'^[\d\w\s\+\-\*\/\(\)\^]+$',
                   message="Invalid function format"),
        ],
    )
    xMin = FloatField(Markup("x<sub>min</sub> ="))
    xMax = FloatField(Markup("x<sub>max</sub> ="))
    submit = SubmitField("Add Function")

    def validate_function(form, field):
        try:
            free_symbols = sp.sympify(field.data).free_symbols
            assert free_symbols <= {sp.symbols('x')}
        except Exception as e:
            raise ValidationError("Not a valid expression.")


class EditFunctionForm(FlaskForm):
    function = StringField(
        Markup("f(x) ="),
        validators=[
            DataRequired(),
            Regexp(r'^[\d\w\s\+\-\*\/\(\)\^]+$',
                   message="Invalid function format"),
        ],
    )
    xMin = FloatField(Markup("x<sub>min</sub> ="))
    xMax = FloatField(Markup("x<sub>max</sub> ="))
    update = SubmitField('Update')
    delete = SubmitField('Delete')

    def validate_function(form, field):
        try:
            free_symbols = sp.sympify(field.data).free_symbols
            assert free_symbols <= {sp.symbols('x')}
        except Exception as e:
            raise ValidationError("Not a valid expression.")

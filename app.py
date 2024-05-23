import numpy as np
import sympy as sp

from flask import Flask, flash, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField 
from wtforms.validators import DataRequired, Regexp
from markupsafe import Markup


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ah-ah-uh-uh'
app.jinja_env.filters['zip'] = zip

functions: list[dict] = []


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


def parse_function(f_expr: str, x_min: float, x_max: float) -> dict:
    x = sp.symbols('x')
    sp_expr = sp.sympify(f_expr)
    f = sp.lambdify(x, sp_expr, 'numpy')

    x_values = np.linspace(x_min, x_max, num=101, endpoint=True)

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


@app.route('/', methods=['GET', 'POST'])
def index():
    add_form = AddFunctionForm()
    edit_forms = [EditFunctionForm(prefix=str(i))
                  for i, _ in enumerate(functions)]

    if add_form.validate_on_submit():
        function = add_form.function.data
        x_min = add_form.xMin.data
        x_max = add_form.xMax.data
        try:
            functions.append(parse_function(function, x_min, x_max))
        except Exception as e:
            flash("Function could not be parsed!")
        else:
            flash("Funcionou, caboclo!")
            return redirect('/')

    for i, form in enumerate(edit_forms):
        if form.update.data and form.validate_on_submit():
            function = form.function.data
            x_min = form.xMin.data
            x_max = form.xMax.data
            try:
                functions[i] = parse_function(function, x_min, x_max)
            except Exception as e:
                flash("Function could not be parsed!")
            else:
                flash("Funcionou, caboclo!")
                return redirect('/')
        elif form.delete.data:
            del functions[i]
            return redirect('/')

    return render_template('index.html', functions=functions,
                           add_form=add_form, edit_forms=edit_forms)


if __name__ == '__main__':
    app.run(debug=True)

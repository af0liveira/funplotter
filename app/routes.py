from flask import flash, render_template, redirect, url_for

from app import app
from app.parsers import parse_function
from app.forms import AddFunctionForm, EditFunctionForm


functions: list[dict] = []

@app.route('/', methods=['GET', 'POST'])
def index():
    add_form = AddFunctionForm()
    edit_forms = [EditFunctionForm(prefix=str(i))
                  for i, _ in enumerate(functions)]

    if add_form.submit.data:
        if add_form.validate_on_submit():
            try:
                function = add_form.function.data
                x_min = add_form.xMin.data
                x_max = add_form.xMax.data
                functions.append(parse_function(function, x_min, x_max))
            except Exception as e:
                flash(f"Unexpected error while adding new function: {e}")
            else:
                return redirect(url_for('index'))

    for i, form in enumerate(edit_forms):
        if form.update.data:
            if form.validate_on_submit():
                try:
                    function = form.function.data
                    x_min = form.xMin.data
                    x_max = form.xMax.data
                    functions[i] = parse_function(function, x_min, x_max)
                except Exception as e:
                    flash(f"Unexpected error while updating function: {e}")
                else:
                    return redirect(url_for('index'))
        elif form.delete.data:
            del functions[i]
            return redirect(url_for('index'))

    return render_template('index.html', functions=functions,
                           add_form=add_form, edit_forms=edit_forms)

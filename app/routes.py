import uuid

from flask import flash, render_template, redirect, session, url_for

from app import app
from app.parsers import parse_function
from app.forms import create_form


functions: list[dict] = []


@app.route('/', methods=['GET', 'POST'])
def index():

    if 'session_id' not in session or 'functions' not in session:
        return redirect(url_for('new_session'))

    session_id = session['session_id']
    functions = session['functions']

    print(f"{session_id=}")

    add_form = create_form('new_function')
    edit_forms = [create_form('function_update', prefix=str(i))
                  for i, _ in enumerate(functions)]

    if add_form.submit.data:
        if add_form.validate_on_submit():
            try:
                function = add_form.function.data
                x_min = add_form.xMin.data
                x_max = add_form.xMax.data
                functions.append(parse_function(function, x_min, x_max))
            except Exception as e:
                flash(f"Unexpected error while adding new function: {e}",
                      category='danger')
            else:
                flash(f"Function added!", category='success')
                return redirect(url_for('index'))
        else:
            flash(f"Function not added!", category='danger')
    else:
        for i, form in enumerate(edit_forms):
            if form.update.data:
                if form.validate_on_submit():
                    try:
                        function = form.function.data
                        x_min = form.xMin.data
                        x_max = form.xMax.data
                        functions[i] = parse_function(function, x_min, x_max)
                    except Exception as e:
                        flash(f"Unexpected error while updating function: {e}",
                              category='danger')
                    else:
                        flash(f"Function updated!", category='success')
                        return redirect(url_for('index'))
                else:
                    flash(f"Function not updated!", category='danger')
                    break
            elif form.delete.data:
                del functions[i]
                flash(f"Function successfully deleted!", category='success')
                return redirect(url_for('index'))

    return render_template('index.html', functions=functions,
                           add_form=add_form, edit_forms=edit_forms)


@app.route('/new_session/')
def new_session():
    new_session_id = str(uuid.uuid4())

    session.clear()
    session['session_id'] = new_session_id
    session['functions']: list[dict] = []

    return redirect(url_for('index'))

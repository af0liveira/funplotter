import uuid

from flask import flash, render_template, redirect, session, url_for

from app import app
from app.forms import create_form
from app.parsers import parse_function_form, ParsingError


functions: list[dict] = []


@app.route('/', methods=['GET', 'POST'])
def index():

    if 'session_id' not in session or 'functions' not in session:
        return redirect(url_for('new_session'))

    session_id = session['session_id']
    functions = session['functions']

    print(f"{session_id=}")

    add_fun_form = create_form('new_function')
    edit_fun_forms = [create_form('function_update', prefix=str(i))
                      for i, _ in enumerate(functions)]

    if add_fun_form.submit.data:
        if add_fun_form.validate_on_submit():
            try:
                functions.append(parse_function_form(add_fun_form))
            except ParsingError:
                pass
            except Exception as e:
                flash(f"Unexpected error: {str(e)}.")
            else:
                return redirect(url_for('index'))
    else:
        for i, form in enumerate(edit_fun_forms):
            if form.update.data:
                if form.validate_on_submit():
                    try:
                        functions[i] = parse_function_form(form)
                    except ParsingError:
                        pass
                    except Exception as e:
                        flash(f"Unexpected error: {str(e)}.")
                    else:
                        return redirect(url_for('index'))
                else:
                    break
            elif form.delete.data:
                del functions[i]
                return redirect(url_for('index'))

    return render_template('index.html', functions=functions,
                           add_form=add_fun_form, edit_forms=edit_fun_forms)


@app.route('/new_session/')
def new_session():
    new_session_id = str(uuid.uuid4())

    session.clear()
    session['session_id'] = new_session_id
    session['functions']: list[dict] = []

    return redirect(url_for('index'))

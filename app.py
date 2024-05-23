import numpy as np

from flask import Flask, jsonify, render_template, redirect, request


app = Flask(__name__)

functions: list[dict]= []

@app.route('/')
def index():
    return render_template('index.html', functions=functions)

@app.route('/add_function/', methods=['POST'])
def add_function():
    function = request.form.get('addFunction')
    x_min = float(request.form.get('setXMin'))
    x_max = float(request.form.get('setXMax'))

    x_values = np.linspace(x_min, x_max, num=101, endpoint=True)
    y_values = eval(function.replace('x', 'x_values'))

    function_dict = {
        'label': function,
        'x_min': x_min,
        'x_max': x_max,
        'data': [{'x': x, 'y': y} for x, y in zip(x_values, y_values)],
    }

    functions.append(function_dict)

    return redirect('/')

@app.route('/delete_function/<int:id>', methods=['POST'])
def delete_function(id: int):
    del functions[id]
    return redirect('/')

@app.route('/update_function/<int:id>', methods=['POST'])
def update_function(id: int):
    function = request.form.get(f'function{id}')
    x_min = float(request.form.get(f'setXMin{id}'))
    x_max = float(request.form.get(f'setXMax{id}'))

    x_values = np.linspace(x_min, x_max, num=101, endpoint=True)
    y_values = eval(function.replace('x', 'x_values'))

    function_dict = {
        'label': function,
        'x_min': x_min,
        'x_max': x_max,
        'data': [{'x': x, 'y': y} for x, y in zip(x_values, y_values)],
    }

    functions[id] = function_dict

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

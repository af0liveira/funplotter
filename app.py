import numpy as np

from flask import Flask, render_template, request, jsonify, redirect


app = Flask(__name__)

functions = []
counter = 0

def _serialize_function(fun:str, x_min: float = -10, x_max: float = 10):
    """Serialize function expression."""
    x_values = np.linspace(x_min, x_max, num=101, endpoint=True)
    y_values = eval(fun.replace('x', 'x_values'))
    ret = {
        'label': fun,
        'data': [{'x': x, 'y': y} for x, y in zip(x_values, y_values)],
        'fill': True,
        'lineTension': 0.1,
    }
    return ret

@app.route('/')
def index():
    """Render page with empty plot."""
    print(f"{functions=}")
    datasets = [_serialize_function(f) for f in functions]
    return render_template('index.html', functions=functions, datasets=datasets)

@app.route('/new', methods=['POST'])
def add_function():
    fun = request.form.get('newFunction')

    if fun:
        functions.append(fun)
    
    print(f"{fun=}")
    print(f"{functions=}")

    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update_function(id):
    print(f"{id=}")
    fun = request.form.get(f'fun{id}')
    print(f"{fun=}")
    print(f"{functions=}")
    if fun:
        functions[id] = fun

    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_function(id):
    del functions[id]
    return redirect('/')
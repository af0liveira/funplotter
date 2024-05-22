import numpy as np

from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    x_values = np.linspace(-10, 10, num=50, endpoint=True)
    y_values = x_values * x_values**2

    data_points = [{'x': x, 'y': y} for x, y in zip(x_values, y_values)]

    return render_template('graph.html', data_points=data_points)

if __name__ == '__main__':
    app.run(debug=True)
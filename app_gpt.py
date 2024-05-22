from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

functions = []

@app.route('/')
def index():
    return render_template('index.html', functions=functions)

@app.route('/add_function', methods=['POST'])
def add_function():
    func = request.form.get('function')
    if func:
        functions.append(func)
    return jsonify(functions)

@app.route('/update_function/<int:index>', methods=['POST'])
def update_function(index):
    func = request.form.get('function')
    if func and 0 <= index < len(functions):
        functions[index] = func
    return jsonify(functions)

@app.route('/delete_function/<int:index>', methods=['POST'])
def delete_function(index):
    if 0 <= index < len(functions):
        functions.pop(index)
    return jsonify(functions)

if __name__ == '__main__':
    app.run(debug=True)

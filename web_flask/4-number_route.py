#!/usr/bin/python3
''' Task 3'''
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    return 'C ' + text.replace('_', ' ')


@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    default_text = text or 'is cool'
    result = f"Python {default_text}"
    return result


@app.route('/number/<int:n>', strict_slashes=False)
def int(n):
    return n + 'is a number'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

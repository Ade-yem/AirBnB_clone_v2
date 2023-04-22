#!/usr/bin/python3
"""module starts web flask application"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """displays the index page"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """displays the hbnb page"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def show_c(text):
    """ display “C ” followed by the value of the text variable"""
    text = escape(text).replace('_', ' ')
    return "C %s" % text


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    """ Function called with /python/<text> route """
    if text != 'is cool':
        text = escape(text).replace('_', ' ')
    return f'Python {text}'


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """show the number with the given id, the id is an integer"""
    return '%d is a number' % n


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

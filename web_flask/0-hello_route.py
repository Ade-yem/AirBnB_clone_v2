#!/usr/bin/python3
"""module starts web flask application"""
from flask import Flask, request

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """displays the index page"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

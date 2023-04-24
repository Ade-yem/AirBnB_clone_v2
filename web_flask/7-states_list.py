#!/usr/env/python3
"""starts a Flask web application listening on  0.0.0.0, port 5000"""
from flask import Flask, render_template
from markupsafe import escape
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def show_states():
    """shows the list of states"""
    objs = storage.all("State")
    return render_template("7-states_list.html", objs=objs)


@app.teardown_appcontext
def close(exception):
    """remove current db session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

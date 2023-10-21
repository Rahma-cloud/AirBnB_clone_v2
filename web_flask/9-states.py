#!/usr/bin/python3
"""Task 9"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__, template_folder="templates")


@app.route("/states", strict_slashes=False)
def states():
    """
    Display a list of states and their cities.
    """
    states = storage.all(State).values()
    return render_template("9-states.html", states=states)


@app.route("/states/<id>", strict_slashes=False)
def list_cities(id):
    """list cities route"""
    key = f"State.{id}"
    states = storage.all(State)
    if key in states:
        state = states[key]
        return render_template("9-states.html", state=state)
    else:
        return render_template("9-states.html", not_found=True)


@app.teardown_appcontext
def teardown(exception):
    """Close the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

#!/usr/bin/python3
"""Task 8"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__, template_folder="templates")


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Display a list of states with their IDs and names"""
    states = storage.all(State).values()
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exception):
    """Close the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

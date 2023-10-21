#!/usr/bin/python3
"""Web Flask Module"""


from flask import Flask, render_template
from models import storage
from models.amenity import Amenity
from models.state import State


app = Flask(__name__, template_folder="templates")


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """hbnb filters route"""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()

    return render_template(
        "10-hbnb_filters.html", states=states, amenities=amenities
        )


@app.teardown_appcontext
def teardown(exception):
    """Close the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

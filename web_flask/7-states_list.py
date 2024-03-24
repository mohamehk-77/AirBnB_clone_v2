#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from models import storage
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False  # Allow URLs with and without trailing slashes


@app.route("/states_list")
def states_list():
    """
    Displays an HTML page with a list of all State objects in DBStorage.
    States are sorted by name (ascending order).
    """
    states = storage.all("State")
    sorted_states = sorted(
        states.values(), key=lambda state: state.name)  # Sort by name
    return render_template("7-states_list.html", states=sorted_states)


@app.teardown_appcontext
def teardown(exc):
    """
    Removes the current SQLAlchemy session after each request.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Specify port explicitly

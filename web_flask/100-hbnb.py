from models import storage
from flask import Flask, render_template

# Optional: Consider adding error handling for imports
try:
    from models import storage
    from flask import Flask, render_template
except ImportError as e:
    print(f"Error importing modules: {e}")
    exit(1)

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/hbnb")
def hbnb():
    """
    Displays the main HBnB page by fetching and rendering State,
    Amenity, and Place objects sorted alphabetically.

    Handles potential errors during data retrieval.
    """
    try:
        states = sorted(storage.all("State").values(),
                        key=lambda state: state.name)
        amenities = sorted(storage.all("Amenity").values(),
                           key=lambda amenity: amenity.name)
        places = sorted(storage.all("Place").values(),
                        key=lambda place: place.name)
    except Exception as e:
        # Handle database access error
        return f"Error retrieving data: {e}", 500

    return render_template(
        "100-hbnb.html",
        states=states,
        amenities=amenities,
        places=places
    )


@app.teardown_appcontext
def teardown(exc):
    """
    Removes the SQLAlchemy session after each request.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

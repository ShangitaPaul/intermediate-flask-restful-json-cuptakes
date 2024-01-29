"""This is the flaks app that creates a web service that allows users to perform various operations on cupcakes, including adding, retrieving, updating, and deleting cupcake data."""

from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

# Configuration for connecting to the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

# Connect the Flask app to the SQLAlchemy database
connect_db(app)

@app.route("/")
def root():
    """Render homepage."""
    
    # Render the index.html template for the homepage
    return render_template("index.html")

@app.route("/api/cupcakes")
def list_cupcakes():
    """Return all cupcakes in the system.

    Returns json like:
        {cupcakes: [{id, flavor, rating, size, image}, ...]}
    """

    # Query all cupcakes from the database and convert them to a list of dictionaries
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]

    # Return the list of cupcakes as JSON
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Adding a cupcake and returns new cupcake info.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    # Get the JSON data from the request
    data = request.json

    # Create a new Cupcake object with the provided data
    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None
    )

    # Add the new cupcake to the database
    db.session.add(cupcake)
    db.session.commit()

    # Return the newly created cupcake as JSON with HTTP status 201 CREATED
    return (jsonify(cupcake=cupcake.to_dict()), 201)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Return data on a specific cupcake.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    # Query the database for the specified cupcake_id
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # Return the data of the specific cupcake as JSON
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake from the data in the request. Return updated data.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    # Get the JSON data from the request
    data = request.json

    # Query the database for the specified cupcake_id
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # Update the cupcake with the new data
    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    # Add the updated cupcake to the database
    db.session.add(cupcake)
    db.session.commit()

    # Return the updated cupcake as JSON
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete a cupcake and return a confirmation message.

    Returns JSON of {message: "Deleted"}
    """

    # Query the database for the specified cupcake_id
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # Delete the cupcake from the database
    db.session.delete(cupcake)
    db.session.commit()

    # Return a confirmation message as JSON
    return jsonify(message="Deleted")

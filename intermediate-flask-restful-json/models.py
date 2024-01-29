"""This is the model code that defines a Flask SQLAlchemy model for cupcakes, specifies the structure of the Cupcake table, and includes a method to convert Cupcake objects to dictionaries for serialization. ."""

# Models for Cupcake app.
from flask_sqlalchemy import SQLAlchemy

# Create a SQLAlchemy instance to handle database operations
db = SQLAlchemy()

# Default image URL for cupcakes
DEFAULT_IMAGE = "https://tinyurl.com/demo-cupcake"

# Define the Cupcake model
class Cupcake(db.Model):
    """Cupcake model representing cupcakes in the database."""

    # Specify the table name in the database
    __tablename__ = "cupcakes"

    # Define columns for the Cupcake table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE)

    def to_dict(self):
        """Serialize cupcake to a dictionary containing cupcake information."""
        # Convert Cupcake object to a dictionary for JSON serialization
        return {
            "id": self.id,
            "flavor": self.flavor,
            "rating": self.rating,
            "size": self.size,
            "image": self.image,
        }

# Function to connect the Flask app to the database
def connect_db(app):
    """Connect to the database."""
    
    # Set the Flask app for the SQLAlchemy instance
    db.app = app
    # Initialize the SQLAlchemy instance with the Flask app
    db.init_app(app)

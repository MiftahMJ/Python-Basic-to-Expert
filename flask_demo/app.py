from flask import Flask, jsonify
from models.user import db
from routes.user_routes import user_bp

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/users')  # Adds a prefix for clarity

# Home route
@app.route('/')
def home():
    return jsonify(message="Welcome to the API!")

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)

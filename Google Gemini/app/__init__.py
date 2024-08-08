import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    # Set configuration variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')

    # Register routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app

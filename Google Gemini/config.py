import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Load environment variables from the .env file
    load_dotenv()

    # Set the secret key for session management
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_fallback_key')

    return app

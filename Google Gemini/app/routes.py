import requests
from flask import Blueprint, request, jsonify, render_template, current_app

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    api_key = current_app.config['GEMINI_API_KEY']

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Define the API endpoint and payload
    api_endpoint = 'https://api.google.com/gemini/chat'  # Replace with the actual endpoint
    payload = {
        'user_message': user_message
    }

    # Make the request to Google Gemini API
    response = requests.post(api_endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code

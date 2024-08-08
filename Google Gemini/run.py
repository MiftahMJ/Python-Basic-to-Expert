from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from GeminiAIChat.core import API

# Load environment variables
load_dotenv()

app = Flask(__name__)
api_key = os.getenv('GEMINI_API_KEY')
gemini_api = API(api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    gemini_api.prompt(user_message)
    response = gemini_api.response()

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

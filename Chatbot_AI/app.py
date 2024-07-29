from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

API_KEY = 'AIzaSyCPWAtZkbk80YM24KRqVXtm-IBzmlUVyns'
API_URL = 'https://api.google.com/generative-ai/v1'  # Hypothetical URL

def get_ai_response(prompt):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gemini-1.5-flash',
        'prompt': prompt,
        'temperature': 1,
        'top_p': 0.95,
        'top_k': 64,
        'max_tokens': 8192
    }
    response = requests.post(f'{API_URL}/generate', json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('text', '')
    return "Error: Unable to fetch response."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response_message = get_ai_response(user_input)
    return jsonify({"message": response_message})

if __name__ == '__main__':
    app.run(debug=True)

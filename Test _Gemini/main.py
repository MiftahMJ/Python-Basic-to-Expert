# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit
# import requests
#
# app = Flask(__name__)
# socketio = SocketIO(app)
#
# # Replace with your actual Gemini API key
# GEMINI_API_KEY = 'AIzaSyCHl7g8gQKOyPhLeAQA96UGkhywQKrMF58'
# GEMINI_API_URL = 'https://api.gemini.com/v1/'
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @socketio.on('message')
# def handle_message(message):
#     print(f"Received message: {message}")
#
#     # Example endpoint for Google Gemini API; adjust as needed
#     endpoint = 'your-endpoint-here'
#     try:
#         response = requests.post(
#             f"{GEMINI_API_URL}{endpoint}",
#             headers={'Authorization': f'Bearer {GEMINI_API_KEY}', 'Content-Type': 'application/json'},
#             json={'message': message}
#         )
#         data = response.json()
#         emit('response', {'data': data}, broadcast=True)
#     except Exception as e:
#         emit('response', {'error': str(e)}, broadcast=True)
#
# if __name__ == '__main__':
#     socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
import requests

api_key = "AIzaSyCHl7g8gQKOyPhLeAQA96UGkhywQKrMF58"
headers = {"Authorization": f"Bearer {api_key}"}
start_chat_url = "https://api.gemini.com/v1/startChat"
send_message_url = "https://api.gemini.com/v1/sendMessage"

# Start a chat
response = requests.post(start_chat_url, headers=headers, json={"history": [...]})
chat_id = response.json()["chat_id"]

# Send a message
response = requests.post(send_message_url, headers=headers, json={"chat_id": chat_id, "message": "I have 2 dogs in my house."})
print(response.json()["text"])

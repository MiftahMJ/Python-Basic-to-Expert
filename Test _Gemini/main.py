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
# import google.generativeai as genai
# import os
#
# genai.configure(api_key=os.environ["API_KEY"])
#
# model = genai.GenerativeModel('gemini-1.5-flash')
# from flask import Flask, request, jsonify, render_template
# import google.generativeai as genai
# import os
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# generation_config={"temperature":0.9,
#                    "top_p":1,
#                    "top_k":1,
#                    "max_output_tokens":2048}
# model=genai.GenerativeModel("gemini-pro",generation_config=generation_config)
# response=model.generate_content(["Create a meal plan for today"])
# print(response.text)
# app = Flask(__name__)

# # Set up your API key and model name
# API_KEY = 'AIzaSyCHl7g8gQKOyPhLeAQA96UGkhywQKrMF58'
# MODEL_NAME = 'gemini-1.5-flash'
#
# # Initialize the GenerativeModel
# model = genai.GenerativeModel(model_name=MODEL_NAME, api_key=API_KEY)
#
# # Route for the homepage
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# # Route for generating text
# @app.route('/generate', methods=['POST'])
# def generate_text():
#     user_input = request.json.get('input', '')
#
#     try:
#         # Generate text using the Gemini model
#         result = model.generate(input=user_input)
#         return jsonify({'output': result})
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({'error': 'Failed to generate text'}), 500
#
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

# Initialize Flask application
app = Flask(__name__)

# Configure API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Generation configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048
}


# Define the route for the homepage
@app.route('/')
def index():
    return render_template('index.html')


# Define the route for generating text
@app.route('/generate', methods=['POST'])
def generate_text():
    user_input = request.json.get('input', '')

    try:
        # Create the Generative Model
        model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)

        # Generate content
        response = model.generate(prompt=user_input)

        # Return generated text
        return jsonify({'output': response['text']})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to generate text'}), 500


if __name__ == '__main__':
    app.run(debug=True)

# CLIENT_ID="1076346442788-o74r5cd0ji0l5lsq4uj3jdblip8i3bdo.apps.googleusercontent.com"
# CLIENT_SECRET="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"
# API_KEY="AIzaSyDFYCkYWVU7a9u_sUSjoM7ghNJzm9WJBZQ"
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
import genai


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
from flask import Flask, request, render_template
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Set your API key directly (replace this with your actual API key)
GOOGLE_API_KEY = 'AIzaSyCHl7g8gQKOyPhLeAQA96UGkhywQKrMF58'  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

def generate_title(focus_keyword):
    prompt = f"""
    Write a compelling blog title focused on '{focus_keyword}' that is both engaging for readers and optimized for SEO.
    Note:
    - Focus keyword used at the beginning of the SEO title.
    - Title must have a positive or negative sentiment.
    - Title must contain a power word or word(s).
    - Use a number in your SEO title.
    - Use a number at the start, and include the latest year in the title.
    Suggest 5 titles.
    """
    try:
        response = genai.generate_text(prompt=prompt)
        if hasattr(response, 'result'):
            titles = response.result.split('\n')  # Split the result by new lines
            # Clean up titles by removing any leading or trailing '**' and extra spaces
            cleaned_titles = [title.strip('*').strip() for title in titles]
            return cleaned_titles
        return ["No titles were generated."]
    except Exception as e:
        return [f"An error occurred: {e}"]

@app.route('/', methods=['GET', 'POST'])
def generate():
    titles = None
    error = None
    if request.method == 'POST':
        focus_keyword = request.form.get('prompt', '')
        if focus_keyword:
            titles = generate_title(focus_keyword)
        else:
            error = "Please enter a focus keyword."
    return render_template('index.html', titles=titles, error=error)

if __name__ == '__main__':
    app.run(debug=True)

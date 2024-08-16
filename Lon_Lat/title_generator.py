# from flask import Flask, request, render_template
# import google.generativeai as genai
#
# # Initialize Flask app
# app = Flask(__name__)
#
# # Set your API key directly (replace this with your actual API key)
# GOOGLE_API_KEY = 'AIzaSyCHl7g8gQKOyPhLeAQA96UGkhywQKrMF58'  # Replace with your actual API key
# genai.configure(api_key=GOOGLE_API_KEY)
#
# def generate_title(focus_keyword):
#     prompt = f"""
#     Write a compelling blog title focused on '{focus_keyword}' that is both engaging for readers and optimized for SEO.
#     Note:
#     - Focus keyword used at the beginning of the SEO title.
#     - Title must have a positive or negative sentiment.
#     - Title must contain a power word or word(s).
#     - Use a number in your SEO title.
#     - Use a number at the start, and include the latest year in the title.
#     Suggest 5 titles.
#     """
#     try:
#         response = genai.generate_text(prompt=prompt)
#         if hasattr(response, 'result'):
#             titles = response.result.split('\n')  # Split the result by new lines
#             # Clean up titles by removing any leading or trailing '**' and extra spaces
#             cleaned_titles = [title.strip('*').strip() for title in titles]
#             return cleaned_titles
#         return ["No titles were generated."]
#     except Exception as e:
#         return [f"An error occurred: {e}"]
#
# @app.route('/', methods=['GET', 'POST'])
# def generate():
#     titles = None
#     error = None
#     if request.method == 'POST':
#         focus_keyword = request.form.get('prompt', '')
#         if focus_keyword:
#             titles = generate_title(focus_keyword)
#         else:
#             error = "Please enter a focus keyword."
#     return render_template('title_generator.html', titles=titles, error=error)
#
# if __name__ == '__main__':
#     app.run(debug=True)
import logging
import google.generativeai as genai
from flask import request, render_template, Flask

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Set your API key directly (replace this with your actual API key)
GOOGLE_API_KEY = 'AIzaSyCHl7g8gQKOyPhLeAQA96UGkhywQKrMF58'
genai.configure(api_key=GOOGLE_API_KEY)

def generate_title(focus_keyword):
    prompt = f"""
    Write a compelling blog title focused on '{focus_keyword}' that is both engaging for readers and optimized for SEO.
    Suggest 5 titles.
    """
    try:
        response = genai.generate_text(prompt=prompt)
        logging.debug(f"API Response: {response}")
        if hasattr(response, 'result'):
            titles = response.result.split('\n')
            cleaned_titles = [title.strip('*').strip() for title in titles]
            return cleaned_titles
        return ["No titles were generated."]
    except Exception as e:
        logging.error(f"An error occurred: {e}")
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
    return render_template('title_generator.html', titles=titles, error=error)

if __name__ == '__main__':
    app.run(debug=True)

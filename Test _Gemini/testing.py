from flask import Flask, request
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Set your API key directly (replace this with your actual API key)
GOOGLE_API_KEY = ''

# Configure the Generative AI API with your API key
genai.configure(api_key=GOOGLE_API_KEY)


def generate_title(prompt):
    """
    Generate a title using the Generative AI API based on the given prompt.
    """
    try:
        # Call the API to generate text based on the prompt
        response = genai.generate_text(prompt=prompt)

        # Adjust based on actual response structure
        if hasattr(response, 'text'):
            return response.text
        elif isinstance(response, dict) and 'text' in response:
            return response['text']
        else:
            return str(response)  # Convert the whole response object to string if no 'text' field

    except Exception as e:
        return f"An error occurred: {e}"


@app.route('/generate', methods=['POST'])
def generate():
    # Get the prompt directly from the request data
    prompt = request.form.get('prompt', '')

    if not prompt:
        return "Please enter a prompt."

    # Generate the title
    title = generate_title(prompt)

    return title


if __name__ == '__main__':
    # Get the prompt from the user in the console
    prompt = input("Enter a keyword or prompt for the title: ")

    # Generate the title
    title = generate_title(prompt)

    # Print the generated title to the console
    print("Generated Title: ", title)

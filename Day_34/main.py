from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
from ui import QuizInterface
import requests
import html

# Define parameters for the API request
parameters = {
    "amount": 10,
    "type": "boolean"
}

# Make the API request and check for errors
response = requests.get("https://opentdb.com/api.php", params=parameters)
response.raise_for_status()
data = response.json()
print(data["results"])

# Create the question bank
question_bank = []
for question in data["results"]:  # Use the data from the API
    question_text = html.unescape(question["question"])  # Unescape HTML entities
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

# Initialize the quiz and quiz interface
quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)

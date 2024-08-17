from flask import Flask
import random
app = Flask(__name__)
# Generate a random number between 0 and 9
random_number = random.randint(0, 9)
def make_bold(func):
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"

    return wrapper

@app.route('/')
def hello_world():
    return '<h1>Guess a number between 0 and 9</h1>'\
           '<img src="https://i.giphy.com/3o7aCSPqXE5C6T8tBC.webp">'

@app.route('/<int:user_guess>')
def guess(user_guess):
    if user_guess < random_number:
        return '<h1 style="text-align: center; color: red">Too low!</h1>'\
    '<img src="https://udemy-images.s3.amazonaws.com/redactor/raw/2020-08-28_08-54-17-e6a9f5748b74b0e2e991692bff518654.png">'

    elif user_guess > random_number:
        return '<h1 style="text-align: center; color: orange">Too high!</h1>'\
    '<img src="https://udemy-images.s3.amazonaws.com/redactor/raw/2020-08-28_08-55-13-107b5d775b8962d211ad30efd5f68a23.png">'
    else:
        return '<h1 style="text-align: center; color: green">You found me!</h1>'\
    '<img src="https://udemy-images.s3.amazonaws.com/redactor/raw/2020-08-28_08-55-54-0448eaca5e97382adab9f551da11913b.png">'

if __name__ == "__main__":
    app.run(debug=True)
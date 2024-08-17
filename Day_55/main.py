from flask import Flask

app = Flask(__name__)


# Define the make_bold decorator
def make_bold(func):
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"

    return wrapper


# Define the make_underline decorator
def make_underline(func):
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args, **kwargs)}</u>"

    return wrapper


@app.route('/')
def hello_world():
    return '<h1 style="text-align: center">Hello World!</h1>' \
           '<p>This is a paragraph</p>'


@app.route("/bye")
@make_bold
@make_underline
def bye():
    return "bye!"


@app.route("/<name>")
def greet(name):
    return f"hello {name}"


class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False


def is_authenticated_decorater(function):
    def wrapper(*args, **kwargs):
        if args[0].is_logged_in == True:
            function(args[0])

    return wrapper()


def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")


new_user = User("miftah")
new_user.is_logged_in == True
create_blog_post(new_user)
if __name__ == "__main__":
    app.run(debug=True)

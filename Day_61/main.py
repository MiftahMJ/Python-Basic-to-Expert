from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap  # Import Bootstrap

app = Flask(__name__)

# Define a secret key for CSRF protection
app.config['SECRET_KEY'] = 'some_secret_string'

# Initialize Flask-Bootstrap
Bootstrap(app)  # Ensure this line is present and correctly initializes Bootstrap

# Define the LoginForm class using FlaskForm
class LoginForm(FlaskForm):
    email = StringField('Email', render_kw={"size": 30})  # Email field with size 30
    password = PasswordField('Password', render_kw={"size": 30})  # Password field with size 30 and password masking
    submit = SubmitField('Login')

# Home route
@app.route("/")
def home():
    return render_template('index.html')

# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Instantiate the LoginForm
    if form.validate_on_submit():  # Check if the form is submitted and valid
        email = form.email.data
        password = form.password.data
        # Check if the credentials match the specified email and password
        if email == "admin@email.com" and password == "12345678":
            return render_template('success.html')  # Show success page
        else:
            return render_template('denied.html')  # Show denied page
    return render_template('login.html', form=form)  # Pass form to the template

if __name__ == '__main__':
    app.run(debug=True)

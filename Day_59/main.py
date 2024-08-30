import smtplib

from flask import Flask, render_template, request
import requests
posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()
OWN_EMAIL = 'your email'
OWN_PASSWORD = 'password'
app = Flask(__name__)

# Fetch the blog posts from the API
posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

@app.route('/')
def get_all_posts():
    # Pass the posts to the template
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/form-entry", methods=["POST"])
def receive_data():
    data = request.form
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")

    print(name)
    print(email)
    print(phone)
    print(message)

    # Return a success message
    return "<h1>Successfully sent your message</h1>"
# @app.route("/post/<int:post_id>")
# def show_post(post_id):
#     # Find the specific post by its ID
#     post = next((post for post in posts if post['id'] == post_id), None)
#     return render_template("post.html", post=post)
def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)
if __name__ == "__main__":
    app.run(debug=True)

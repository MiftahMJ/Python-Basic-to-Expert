from flask import Flask, render_template
import requests

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

# @app.route("/post/<int:post_id>")
# def show_post(post_id):
#     # Find the specific post by its ID
#     post = next((post for post in posts if post['id'] == post_id), None)
#     return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def receive_data():
    # Here, you can access the submitted form data using request.form.get()
    name = request.form.get('name')
    password = request.form.get('password')

    print("Data submitted")  # This will print to the console

    # Returning a simple response back to the user
    return f"Form submitted! Name: {name}, Password: {password}"


if __name__ == "__main__":
    app.run(debug=True)

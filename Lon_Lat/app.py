# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = '9b8e6c2f4a72e1b6a6e8d3d90b9f3e72'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
#
# # User model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), nullable=False, unique=True)
#     email = db.Column(db.String(150), nullable=False, unique=True)
#     password = db.Column(db.String(200), nullable=False)
#
# # Create the database
# with app.app_context():
#     db.create_all()
#
# # Signup route
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
#
#         user = User(username=username, email=email, password=password)
#         db.session.add(user)
#         db.session.commit()
#
#         flash('Account created successfully! You can now log in.', 'success')
#         return redirect(url_for('login'))
#
#     return render_template('signup.html')
#
# # Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = User.query.filter_by(email=email).first()
#
#         if user and bcrypt.check_password_hash(user.password, password):
#             session['user_id'] = user.id
#             session['username'] = user.username
#             flash('Login successful!', 'success')
#             return redirect(url_for('index'))
#         else:
#             flash('Login failed. Check your email and password.', 'danger')
#
#     return render_template('login.html')
#
# # Main UI route (after login)
# @app.route('/main_ui')
# def main_ui():
#     if 'user_id' not in session:
#         flash('Please log in to access this page.', 'danger')
#         return redirect(url_for('login'))
#
#     return render_template('main_ui.html', username=session['username'])
#
# # Logout route
# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     session.pop('username', None)
#     flash('You have been logged out.', 'success')
#     return redirect(url_for('login'))
# @app.route('/')
# def home():
#     return redirect(url_for('signup'))
#
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '9b8e6c2f4a72e1b6a6e8d3d90b9f3e72'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to the 'index' route
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('login.html')

# Index route (to render index.html)
@app.route('/index')
def index():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

    return render_template('index.html', username=session['username'])

# SEO Tool route (example)
@app.route('/seo_tool')
def seo_tool():
    return render_template('seo_tool.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/')
def home():
    return redirect(url_for('signup'))

if __name__ == '__main__':
    app.run(debug=True)

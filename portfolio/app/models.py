# app/models.py

from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    badge = db.Column(db.String(20), default='None')  # Silver, Golden, or None

    portfolios = db.relationship('Portfolio', backref='author', lazy=True)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    youtube_link = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    relevant_links = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class SignUpRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(10), default='Pending')  # Pending, Approved, Rejected

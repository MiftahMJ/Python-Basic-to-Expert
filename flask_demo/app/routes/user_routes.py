from flask import Blueprint, request, jsonify
from .. import db
from ..models.user import User

user_bp = Blueprint('users', __name__)

# Create a User (POST /api/users)
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    new_user = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'id': new_user.id,
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
        'email': new_user.email
    }), 201

# Get all Users (GET /api/users)
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users]
    return jsonify(result), 200

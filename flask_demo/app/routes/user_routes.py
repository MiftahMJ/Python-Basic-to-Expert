
from flask import Blueprint, request, jsonify
from .. import db  # Import db from the app package (using relative import)
from ..models.user import User  # Import the User model

user_bp = Blueprint('users', __name__)

# Create a User (POST /users)
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Extract data and validate
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    if not first_name or not last_name or not email:
        return jsonify({'error': 'Missing required fields'}), 400

    # Ensure the email is unique
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    # Create and save the new user
    new_user = User(first_name=first_name, last_name=last_name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'id': new_user.id,
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
        'email': new_user.email,
        'created_at': new_user.created_at,
        'updated_at': new_user.updated_at
    }), 201

# Get a List of Users with Pagination (GET /users)
@user_bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    users = User.query.paginate(page=page, per_page=per_page, error_out=False)

    response = {
        'users': [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        } for user in users.items],
        'total': users.total,
        'page': users.page,
        'per_page': users.per_page,
        'total_pages': users.pages
    }
    return jsonify(response), 200

# Get a Single User (GET /users/<id>)
@user_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    }), 200

# Update a User (PUT /users/<id>)
@user_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    # Update user details
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    new_email = data.get('email', user.email)

    # Check if email already exists (and is not the current user’s email)
    if new_email != user.email and User.query.filter_by(email=new_email).first():
        return jsonify({'error': 'Email already exists'}), 400

    user.email = new_email

    db.session.commit()

    return jsonify({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    }), 200

# Delete a User (DELETE /users/<int:id>)
@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return '', 204

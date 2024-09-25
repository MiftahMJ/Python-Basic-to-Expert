from flask import Blueprint, request, jsonify
from models.user import User, db
from schemas.user_schema import UserSchema
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user_data = user_schema.load(data)
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email']
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Email already exists"}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500


@user_bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Correct way to use paginate method
    users_pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)

    # Serialize the data (assuming you have a users_schema for serialization)
    users = users_schema.dump(users_pagination.items)

    return jsonify({
        'users': users,
        'total': users_pagination.total,
        'page': users_pagination.page,
        'per_page': users_pagination.per_page,
        'total_pages': users_pagination.pages
    })


@user_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return user_schema.dump(user)
    else:
        return jsonify({"message": "User not found"}), 404


@user_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if user:
        try:
            user_data = user_schema.load(data, partial=True)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)

            db.session.commit()
            return user_schema.dump(user)
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Email already exists"}), 400
        except Exception as e:
            return jsonify({"message": str(e)}), 500
    else:
        return jsonify({"message": "User not found"}), 404


@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return '', 204
    else:
        return jsonify({"message": "User not found"}), 404

from flask import request, jsonify, Blueprint, make_response

from flaskr.auth import token_required
from flaskr.companies import get_all_companies
from flaskr.models import User
from werkzeug.security import generate_password_hash
from flaskr.database import db

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route('/companies', methods=['GET'])
@token_required
def get_user_companies(current_user):
    companies = get_all_companies(request, current_user)
    return jsonify(companies), 200


@bp.route('/own', methods=['GET'])
@token_required
def get_auth_user(current_user):
    response = {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "is_blocked": current_user.is_blocked,
        "is_staff": current_user.is_staff,
        "ava_url": current_user.ava_url,
        "date_joined": current_user.date_joined,
        "email": current_user.email,
        "phone_number": current_user.phone_number,
    }
    return jsonify(response), 200


@bp.route('/<user_id>', methods=['GET'])
@token_required
def get_user_by_id(current_user, user_id):
    user = User.query.get(user_id)
    if user is None:
        return make_response(f'User with id {user_id} does not exist', 400)
    else:
        response = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_blocked": user.is_blocked,
            "is_staff": user.is_staff,
            "ava_url": user.ava_url,
            "date_joined": user.date_joined,
            "email": user.email,
            "phone_number": user.phone_number,
        }
    return jsonify(response), 200


@bp.route('/<user_id>', methods=['PUT'])
@token_required
def change_user_by_id(current_user, user_id):
    user = User.query.get(user_id)
    if user is None:
        return make_response(f'User with id {user_id} does not exist', 400)
    else:
        data = request.get_json()
        new_first_name = data["first_name"]
        new_last_name = data["last_name"]
        new_password = data["password"]
        new_email = data["email"]
        new_phone_number = data["phone_number"]
        if new_first_name is not None:
            user.first_name = new_first_name
        if new_last_name is not None:
            user.last_name = new_last_name
        if new_password is not None:
            user.password = new_password
        if new_email is not None:
            user.email = new_email
        if new_phone_number is not None:
            user.phone_number = new_phone_number
        db.session.commit()
        response = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_blocked": user.is_blocked,
            "is_staff": user.is_staff,
            "ava_url": user.ava_url,
            "date_joined": user.date_joined,
            "email": user.email,
            "phone_number": user.phone_number,
        }

    return jsonify(response), 200


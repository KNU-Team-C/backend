from flask import request, jsonify, Blueprint, make_response

from flaskr.auth import token_required
from flaskr.companies import get_all_companies
from flaskr.database import db
from flaskr.models import User

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
        response = user.get_info()
    return jsonify(response), 200


@bp.route('/<user_id>', methods=['PUT'])
@token_required
def change_user_by_id(current_user, user_id):
    if not current_user.is_staff and current_user.id != user_id:
        return make_response(jsonify({'error': 'No permissions to perform action'}), 400)

    query = db.session.query(User)
    user = query.filter(User.id == user_id).first()

    if user is None:
        return make_response(jsonify({'error': f'User with id {user_id} does not exist'}), 400)

    data = request.get_json()
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.email = data["email"]
    user.phone_number = data["phone_number"]

    db.session.commit()

    return jsonify(user.get_info()), 200

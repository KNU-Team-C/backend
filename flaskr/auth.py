import datetime
import os
from functools import wraps

import jwt
from flask import request, jsonify, make_response, Blueprint
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from flaskr.database import db
from flaskr.models import User

bp = Blueprint("auth", __name__, url_prefix="/")


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['public_id']).first()
        except:
            return jsonify({'message': f'token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorator


@bp.route("/login", methods=["POST"])
def login():
    auth = request.form
    if not auth or not auth.get("email", None) or not auth.get("password", None):
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    user = User.query.filter_by(email=auth["email"]).first()
    if check_password_hash(user.password, auth["password"]):
        token = jwt.encode(
            {'public_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
            os.getenv('SECRET_KEY'), "HS256")

        response = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "token": token,
        }
        return jsonify(response)

    return make_response('could not verify', 401, {'Authentication': '"login required"'})


@bp.route("/signup", methods=["POST"])
def signup():
    data = request.form
    first_name = data["first_name"]
    last_name = data["last_name"]
    password = data["password"]
    email = data["email"]
    phone_number = data["phone_number"]

    user = User(first_name=first_name, last_name=last_name, password=password, email=email,
                phone_number=phone_number)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return make_response('Such email was registered', 409)

    token = jwt.encode(
        {'public_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
        os.getenv('SECRET_KEY'), "HS256")

    response = {
        "id": user.id,
        "first_name": first_name,
        "last_name": last_name,
        "is_blocked": user.is_blocked,
        "is_staff": user.is_staff,
        "ava_url": user.ava_url,
        "date_joined": user.date_joined,
        "email": email,
        "phone_number": phone_number,
        "token": token,
    }
    return jsonify(response)

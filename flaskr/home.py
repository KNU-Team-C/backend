from flask import request, jsonify, Blueprint, make_response
from flaskr.models import Company
from flaskr.database import db
from flaskr.auth import token_required

bp = Blueprint("home", __name__, url_prefix="/home")


@bp.route("/create_company", methods=["POST"])
@token_required
def create_company(user):
    data = request.form
    name = data["name"]
    email = data["email"]
    address = data["address"]
    phone_number = data["phone_number"]
    employees_num = data["employees_num"]
    location = data["location"]
    description = data["description"]
    company = Company(name=name, email=email, address=address, phone_number=phone_number,
                      employees_num=employees_num, location=location, description=description, user_id=user.id)
    db.session.add(company)
    db.session.commit()

    response = company.get_info()
    return jsonify(response)


@bp.route("/company_info", methods=["GET"])
def company_info():
    data = request.args
    company = Company.query.get(data["id"])
    if company is None:
        return make_response('Such company does not exist', 400)
    else:
        response = company.get_info()
    return jsonify(response)


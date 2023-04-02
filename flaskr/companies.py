from flask import request, jsonify, Blueprint, make_response
from sqlalchemy import text

from flaskr.auth import token_required
from flaskr.database import db
from flaskr.models import Company, Project, Industry, Technology
from flaskr.utils import string_arg_to_ids_list, flat_map, filter_by_text

bp = Blueprint("companies", __name__, url_prefix="/companies")


@bp.route("", methods=["POST"])
@token_required
def create_company(user):
    data = request.get_json()
    name = data['name']
    email = data['email']
    address = data['address']
    phone_number = data['phoneNumber']
    employees_num = data['employeesNum']
    location = data['location']
    description = data['description']
    company = Company(name=name, email=email, address=address, phone_number=phone_number,
                      employees_num=employees_num, location=location,
                      description=description, user_id=user.id)
    db.session.add(company)
    db.session.commit()

    response = company.get_info()
    return jsonify(response)


@bp.route("/<company_id>", methods=["GET"])
def company_info(company_id):
    company = Company.query.get(company_id)
    if company is None:
        return make_response(f'Company with id {company_id} does not exist', 400)
    else:
        response = company.get_info()
    return jsonify(response)


@bp.route('', methods=['GET'])
def get_companies():
    companies = get_all_companies(request)
    return jsonify(companies), 200


@bp.route('/<company_id>', methods=['GET'])
def get_company(company_id):
    query = db.session.query(Company)
    company = query.filter(Company.id == company_id).first()    
    return jsonify(company.get_info()), 200


@bp.route('/<company_id>', methods=['PUT'])
def edit_company(company_id):
    
    
    query = db.session.query(Company)
    name = request.args.get('name', '', type=str)
    email = request.args.get('email', '', type=str)
    phone = request.args.get('phone_number', '', type=str)
    loc = request.args.get('location', '', type=str)
    desc = request.args.get('description', '', type=str)

    company = query.filter(Company.id == company_id).first()
    company.name = name if name is not None and name != '' else company.name
    company.email = email if email is not None and email !='' else company.email
    company.phone_number = phone if phone is not None and phone!='' else company.phone_number
    company.location = loc if loc is not None and loc !='' else company.location
    company.description = desc if desc is not None and desc !='' else company.description

    db.session.commit()

    return jsonify({'message': f'SUCCESS'}),200


def get_all_companies(request, user=None):
    search_query = request.args.get('search_query', '', type=str)

    industries_ids = string_arg_to_ids_list(request.args.get('industries_ids', '', type=str))
    technologies_ids = string_arg_to_ids_list(request.args.get('technologies_ids', '', type=str))

    query = db.session.query(Company)
    query = filter_by_text(search_query, query)

    if (user is not None):
        query = query.filter(text("user_id = :user_id").params(user_id=user.id))

    if len(industries_ids) > 0:
        query = query.filter(
            Company.projects.any(
                Project.industries.any(
                    Industry.id.in_(industries_ids)
                )
            )
        )
    if len(technologies_ids) > 0:
        query = query.filter(
            Company.projects.any(
                Project.technologies.any(
                    Technology.id.in_(technologies_ids)
                )
            )
        )

    companies = query.all()
    result = [company.get_info() for company in companies]
    return result

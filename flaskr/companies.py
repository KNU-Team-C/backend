from flask import request, jsonify, Blueprint, make_response
from sqlalchemy import text

from flaskr.auth import token_required
from flaskr.database import db
from flaskr.external_services import upload_image
from flaskr.models import Company, Project, Industry, Technology
from flaskr.projects import get_all_projects
from flaskr.utils import string_arg_to_ids_list, filter_by_text

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

    result = company.get_info()
    return jsonify(result), 200


@bp.route('/<company_id>/projects', methods=['GET'])
def get_company_projects(company_id):
    return get_all_projects(request, company_id), 200


@bp.route('/<company_id>', methods=['PUT'])
def edit_company(company_id):   
    
    query = db.session.query(Company)
    name = request.args.get('name', '', type=str)
    email = request.args.get('email', '', type=str)
    phone = request.args.get('phone_number', '', type=str)
    loc = request.args.get('location', '', type=str)
    desc = request.args.get('description', '', type=str)
    logo_url = request.args.get('logo_url', '', type=str)

    company = query.filter(Company.id == company_id).first()
    if company.name!=name and name is not None and name != '':
        company.is_verified = False
    company.name = name if name is not None and name != '' else company.name
    company.email = email if email is not None and email !='' else company.email
    company.phone_number = phone if phone is not None and phone!='' else company.phone_number
    company.location = loc if loc is not None and loc !='' else company.location
    company.description = desc if desc is not None and desc !='' else company.description
    company.logo_url = logo_url if logo_url is not None and logo_url !='' else company.logo_url
    db.session.commit()

    

    return jsonify(company.get_info()), 200


@bp.route('/<company_id>/image', methods=['POST'])
@token_required
def upload_company_image(current_user, company_id):
    file = request.files['file']

    query = db.session.query(Company)
    company = query.filter(Company.id == company_id).first()

    if not company:
        return jsonify({'error': 'Company was not found'}), 404

    if current_user.id != company.user_id:
        return jsonify({'error': 'Insufficient permissions to perform action'}), 403

    response = upload_image(file)
    if response.status_code != 200:
        return jsonify({'error': 'Could not upload image'})

    company.logo_url = response.json()['image']['url']
    db.session.commit()

    return jsonify(company.get_info())


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

    companies = query.order_by(Company.date_created.desc()).all()
    result = [company.get_info() for company in companies]
    return result

from flask import request, jsonify, make_response, Blueprint

from flaskr.models import Industry, industries, Technology, Company, CompanyReport, Project
from flaskr.database import db
from sqlalchemy import text

from flaskr.utils import string_arg_to_ids_list, flat_map

bp = Blueprint("admin_companies", __name__, url_prefix="/admin")


@bp.route('/company/<company_id>/verify_request_cancel', methods=['POST'])
def verify_request_cancel(company_id):
    query = db.session.query(Company)

    company = query.filter(Company.id == company_id).first()
    company.is_verification_request_pending = False

    db.session.commit()

    return jsonify({}), 200


@bp.route('/company/<company_id>/verify', methods=['POST'])
def verify_company(company_id):
    query = db.session.query(Company)

    company = query.filter(Company.id == company_id).first()
    company.is_verified = True

    db.session.commit()

    return jsonify({}), 200


@bp.route('/companies', methods=['GET'])
def get_companies():
    """
    Accepting following query parameters:
    statuses - statuses of companies to get. Possible values: 'banned', 'reported', none.
        Values represented as string and can be concatenated in any way
    page - number of the page
    page_size - size of each page
    search_query - search query for users
    industries_ids - industries
    technologies_ids - technologies
    """
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    statuses = request.args.get('statuses', '', type=str)
    search_query = request.args.get('search_query', '', type=str)
    industries_ids = string_arg_to_ids_list(request.args.get('industries_ids', '', type=str))
    technologies_ids = string_arg_to_ids_list(request.args.get('technologies_ids', '', type=str))

    query = db.session.query(Company)
    if 'banned' in statuses:
        query = query.filter(Company.is_blocked)
    if 'reported' in statuses:
        subquery = db.session.query(CompanyReport.company_id).filter(CompanyReport.company_id == Company.id).exists()
        query = query.filter(subquery)

    if len(search_query) > 0:
        query = query.filter(text("name LIKE :query").params(query='%' + search_query + '%'))

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

    query.filter(Company.is_verification_request_pending == True)

    companies = query.order_by(Company.date_created.desc()).paginate(page=page, per_page=page_size)

    result = {
        'total_pages': companies.pages,
        'total_items': companies.total,
        'items_per_page': companies.per_page,
        'current_page': companies.page,
        'companies': [{
            'id': company.id,
            'ava_url': company.logo_url,
            'name': company.name,
            'description': company.description,
            'is_verified': company.is_verified,
            'industries': [{
                'id': industry.id,
                'name': industry.name
            } for industry in flat_map(lambda project: project.industries, company.projects)],
            'technologies': [{
                'id': technology.id,
                'name': technology.name
            } for technology in flat_map(lambda project: project.technologies, company.projects)],
        } for company in companies.items]
    }

    return jsonify(result), 200


@bp.route("/technologies", methods=["GET"])
def get_technologies():
    """
    Accepting following query parameters:
    type - type of users to get amount. Possible values: 'banned', 'reported', none
    """
    all_technologies = db.session.query(Technology).all()
    response = ({
        'id': technology.id,
        'name': technology.name,
        'amount': db.session.query(industries).filter_by(technology_id=technology.id).count()
    } for technology in all_technologies)
    return make_response(jsonify(response), 200)


@bp.route("/industries", methods=["GET"])
def get_industries():
    """
    Accepting following query parameters:
    type - type of users to get amount. Possible values: 'banned', 'reported', none
    """
    all_industries = db.session.query(Industry).all()
    response = ({
        'id': industry.id,
        'name': industry.name,
        'amount': db.session.query(industries).filter_by(industry_id=industry.id).count()
    } for industry in all_industries)
    return make_response(jsonify(response), 200)

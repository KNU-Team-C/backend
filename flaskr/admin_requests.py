from flask import request, jsonify, make_response, Blueprint

from flaskr.models import User, UserReport, Company, CompanyReport
from flaskr.database import db
from sqlalchemy import text, or_

bp = Blueprint("admin_requests", __name__, url_prefix="/admin")


@bp.route('/requests_companies', methods=['GET'])
def get_requests_companies():
    """
    Accepting following query parameters:
    types - types of items to get. Possible values: 'verification', 'reports', none.
        Values represented as string and can be concatenated in any way
    page - number of the page
    page_size - size of each page
    search_query - search query for users

    Returning companies that had been reported and/or are not verified (depending on types passed)
    """
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    types = request.args.get('types', '', type=str)
    search_query = request.args.get('search_query', '', type=str)

    query = db.session.query(Company)
    filters = []
    if 'verification' in types or not types:
        filters.append(Company.is_verified == False)
    if 'reports' in types or not types:
        subquery = db.session.query(CompanyReport.company_id).filter(
            CompanyReport.company_id == Company.id).exists()
        filters.append(subquery)

    if len(filters) > 0:
        query = query.filter(or_(*filters))

    if search_query:
        query = query.filter(text("name LIKE :query").params(query='%' + search_query + '%'))

    query.filter(Company.is_verification_request_pending == True)

    query = query.order_by(Company.date_created)

    companies = query.paginate(page=page, per_page=page_size)

    result = {
        'total_pages': companies.pages,
        'total_items': companies.total,
        'items_per_page': companies.per_page,
        'current_page': companies.page,
        'items': [{
            'id': company.id,
            'type': 'Company',
            'ava_url': company.logo_url,
            'is_verified': company.is_verified,
            'name': company.name,
            'description': company.description,
            'industries': [{
                'id': industry.id,
                'name': industry.name
            } for industry in flat_map(lambda project: project.industries, company.projects)],
            'technologies': [{
                'id': technology.id,
                'name': technology.name
            } for technology in flat_map(lambda project: project.technologies, company.projects)],
            "reports": [{
                'id': report.id,
                'message': report.report_message,
            } for report in company.companyReports]
        } for company in companies.items]
    }
    return jsonify(result), 200


@bp.route('/requests_users', methods=['GET'])
def get_requests_users():
    """
    Accepting following query parameters:
    page - number of the page
    page_size - size of each page
    search_query - search query for users

    Returning users that had been reported
    """
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    search_query = request.args.get('search_query', '', type=str)

    subquery = db.session.query(UserReport.id).filter(UserReport.reported_user_id == User.id).exists()
    query = db.session.query(User).filter(subquery)

    if search_query:
        query = query.filter(text("name LIKE :query").params(query='%' + search_query + '%'))

    query = query.order_by(User.date_joined)

    users = query.paginate(page=page, per_page=page_size)

    result = {
        'total_pages': users.pages,
        'total_items': users.total,
        'items_per_page': users.per_page,
        'current_page': users.page,
        'items': [{
            'id': user.id,
            'type': 'User',
            'ava_url': user.ava_url,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'companies': [{
                'id': company.id,
                'name': company.name
            } for company in user.companies],
            "reports": [{
                'id': report.id,
                'message': report.report_message,
            } for report in user.userReportsReported]
        } for user in users.items]
    }
    return jsonify(result), 200


flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]


@bp.route("/requests_amount", methods=["GET"])
def get_filtered_requests():
    """
    Accepting following query parameters:
    type - type of requests to get amount. Possible values: 'verification', 'reports'
    """
    type_arg = request.args.get("type")
    if type_arg == "verification":
        amount = db.session.query(Company.id).filter_by(is_verified=False).count()
    elif type_arg == "reports":
        companies_subquery = db.session.query(CompanyReport.company_id).filter(
            CompanyReport.company_id == CompanyReport.id).exists()
        users_subquery = db.session.query(UserReport.reported_user_id).filter(
            UserReport.reported_user_id == User.id).exists()
        users_amount = db.session.query(User.id).filter(users_subquery).count()
        companies_amount = db.session.query(Company.id).filter(companies_subquery).count()
        amount = users_amount + companies_amount
    else:
        return make_response('Such type parameter is not allowed', 400)
    response = {
        'amount': amount
    }
    return make_response(jsonify(response), 200)

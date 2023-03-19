from flask import request, jsonify, make_response, Blueprint

from flaskr.models import User, UserReport, Company, CompanyReport
from flaskr.database import db
from sqlalchemy import text

bp = Blueprint("admin_requests", __name__, url_prefix="/admin")


# THIS REQUEST WORKS INCORRECTLY
@bp.route('/requests', methods=['GET'])
def get_requests():
    """
    Accepting following query parameters:
    types - types of items to get. Possible values: 'verification', 'reports', none.
        Values represented as string and can be concatenated in any way
    page - number of the page
    page_size - size of each page
    search_query - search query for users
    is_users_enabled - should include users into answer
    is_companies_enabled - should include companies into answer
    """
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    types = request.args.get('types', '', type=str)
    search_query = request.args.get('search_query', '', type=str)
    is_users_enabled = request.args.get('is_users_enabled', "", type=str).lower() == "true"
    is_companies_enabled = request.args.get('is_companies_enabled', "", type=str).lower() == "true"

    companies_query = db.session.query(Company)
    users_query = db.session.query(User)
    if 'verification' in types or not types:
        companies_query = companies_query.filter(not Company.is_verified)
    if 'reports' in types or not types:
        companies_subquery = db.session.query(CompanyReport.company_id).filter(
            CompanyReport.company_id == CompanyReport.id).exists()
        companies_query = companies_query.filter(companies_subquery)
        users_subquery = db.session.query(UserReport.reported_user_id).filter(
            UserReport.reported_user_id == User.id).exists()
        users_query = users_query.filter(users_subquery)

    if search_query:
        users_query = users_query.filter(
            text("first_name || ' ' || last_name LIKE :query").params(query='%' + search_query + '%'))
        companies_query = companies_query.filter(text("name LIKE :query").params(query='%' + search_query + '%'))

    companies_query = companies_query.order_by(Company.date_created)
    users_query = users_query.order_by(User.date_joined)
    if is_users_enabled == is_companies_enabled:
        query = users_query.join(companies_query, User.id != Company.id, isouter=True,
                                 full=True)
    elif is_users_enabled:
        query = users_query
    elif is_companies_enabled:
        query = companies_query
    else:
        return jsonify({}), 200

    items = query.paginate(page=page, per_page=page_size)

    result = {
        'total_pages': items.pages,
        'total_items': items.total,
        'items_per_page': items.per_page,
        'current_page': items.page,
        'items': [map_item_to_response(item) for item in items.items]
    }

    return jsonify(result), 200


def map_item_to_response(item):
    print(item)
    if type(item) is Company:
        return {
            'id': item.id,
            'type': 'Company',
            'ava_url': item.logo_url,
            'name': item.name,
            'description': item.description,
            'industries': [{
                'id': industry.id,
                'name': industry.name
            } for industry in flat_map(lambda project: project.industries, item.projects)],
            'technologies': [{
                'id': technology.id,
                'name': technology.name
            } for technology in flat_map(lambda project: project.technologies, item.projects)],
        }
    elif type(item) is User:
        return {
            'id': item.id,
            'type': 'User',
            'ava_url': item.ava_url,
            'first_name': item.first_name,
            'last_name': item.last_name,
            'companies': [{
                'id': company.id,
                'name': company.name
            } for company in item.companies]
        }
    print(str(item) + str(type(item) is User) + ' ' + str(type(item)) + 'not returned')


flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]


@bp.route("/requests_amount", methods=["GET"])
def get_filtered_requests():
    """
    Accepting following query parameters:
    type - type of requests to get amount. Possible values: 'verification', 'reports', none
    """
    type_arg = request.args.get("type")
    if type_arg == "banned":
        amount = db.session.query(User.id).filter_by(is_blocked=True).count()
    elif type_arg == "reported":
        companies_subquery = db.session.query(CompanyReport.company_id).filter(
            CompanyReport.company_id == CompanyReport.id).exists()
        users_subquery = db.session.query(UserReport.reported_user_id).filter(
            UserReport.reported_user_id == User.id).exists()
        users_amount = db.session.query(User.id).filter(users_subquery).count()
        companies_amount = db.session.query(Company.id).filter(companies_subquery).count()
        print(str(users_amount) + " " + str(companies_amount))
        amount = users_amount + companies_amount
    else:
        return make_response('Such type parameter is not allowed', 400)
    response = {
        'amount': amount
    }
    return make_response(jsonify(response), 200)

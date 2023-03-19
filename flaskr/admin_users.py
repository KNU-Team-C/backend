from flask import request, jsonify, make_response, Blueprint
from werkzeug.security import check_password_hash

from flaskr.auth import token_required
from flaskr.models import User, UserReport
from flaskr.database import db
import datetime
import os
from sqlalchemy import exists, func, text

bp = Blueprint("admin_users", __name__, url_prefix="/admin")


@bp.route('/users', methods=['GET'])
def get_users():
    """
    Accepting following query parameters:
    types - types of users to get amount. Possible values: 'banned', 'reported', none.
        Values represented as string and can be concatenated in any way
    page - number of the page
    page_size - size of each page
    search_query - search query for users
    """
    # Retrieve the page number and page size from the request parameters
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    types = request.args.get('types', '', type=str)
    search_query = request.args.get('search_query', '', type=str)

    query = db.session.query(User)
    if 'banned' in types:
        query = query.filter(User.is_blocked)
    if 'reported' in types:
        subquery = db.session.query(UserReport.reported_user_id).filter(UserReport.reported_user_id == User.id).exists()
        query = query.filter(subquery)

    if search_query:
        query = query.filter(text("first_name || ' ' || last_name LIKE :query").params(query='%'+search_query+'%'))

    # Query the database to retrieve the users for the requested page
    users = query.paginate(page=page, per_page=page_size)

    # Serialize the users to JSON format
    result = {
        'total_pages': users.pages,
        'total_items': users.total,
        'items_per_page': users.per_page,
        'current_page': users.page,
        'users': [{
            'id': user.id,
            'ava_url': user.ava_url,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'companies': [{
                'id': company.id,
                'name': company.name
            } for company in user.companies]
        } for user in users.items]
    }

    # Return the serialized result as a JSON response
    return jsonify(result), 200


@bp.route("/users_amount", methods=["GET"])
def get_filtered_users():
    """
    Accepting following query parameters:
    type - type of users to get amount. Possible values: 'banned', 'reported', none
    """
    type_arg = request.args.get("type")
    users = filter_users_query(type_arg)
    if users is None:
        return make_response('Such type parameter is not allowed', 400)
    amount = users.count()
    response = {
        'amount': amount
    }
    return make_response(jsonify(response), 200)


def filter_users_query(type_arg):
    if type_arg is None:
        users = User.query
    elif type_arg == "banned":
        users = get_blocked_users_query()
    elif type_arg == "reported":
        users = get_reported_users_query()
    else:
        users = None
    return users


def get_blocked_users_query():
    return User.query.filter_by(is_blocked=True)


def get_reported_users_query():
    subquery = db.session.query(UserReport.reported_user_id).filter(UserReport.reported_user_id == User.id).exists()
    return db.session.query(User.id).filter(subquery)

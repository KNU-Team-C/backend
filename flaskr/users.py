from flask import request, jsonify, Blueprint

from flaskr.auth import token_required
from flaskr.companies import get_all_companies

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route('/companies', methods=['GET'])
@token_required
def get_user_companies(current_user):
    companies = get_all_companies(request, current_user)
    return jsonify(companies), 200

from flask import jsonify, Blueprint, make_response, request

from flaskr.auth import token_required
from flaskr.database import db
from flaskr.models import Industry
from flaskr.utils import filter_by_text

bp = Blueprint("industries", __name__, url_prefix="/industries")


@bp.route('', methods=['GET'])
def get_industries():
    search_query = request.args.get('search_query', '', type=str)
    query = db.session.query(Industry)
    query = filter_by_text(search_query, query)
    industries = query.all()
    response = [industry.get_info() for industry in industries]
    return jsonify(response), 200


@bp.route('', methods=['POST'])
@token_required
def create_industry(current_user):
    if not current_user.is_staff:
        return make_response('Insufficient rights to create industry', 403)
    data = request.get_json()
    name = data['name']
    industry = Industry(name=name)
    db.session.add(industry)
    db.session.commit()

    response = industry.get_info()
    return jsonify(response), 200

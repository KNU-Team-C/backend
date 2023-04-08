from flask import jsonify, Blueprint, make_response, request

from flaskr.auth import token_required
from flaskr.database import db
from flaskr.models import Technology
from flaskr.utils import filter_by_text

bp = Blueprint("technologies", __name__, url_prefix="/technologies")


@bp.route('', methods=['GET'])
def get_technologies():
    search_query = request.args.get('search_query', '', type=str)
    query = db.session.query(Technology)
    query = filter_by_text(search_query, query)
    technologies = query.all()
    response = [technology.get_info() for technology in technologies]
    return jsonify(response), 200


@bp.route('', methods=['POST'])
@token_required
def create_technology(current_user):
    if not current_user.is_staff:
        return make_response('Insufficient rights to create technology', 403)
    data = request.get_json()
    name = data['name']
    technology = Technology(name=name)
    db.session.add(technology)
    db.session.commit()

    response = technology.get_info()
    return jsonify(response), 200

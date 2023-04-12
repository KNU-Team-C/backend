from flask import jsonify, Blueprint, request, make_response

from flaskr.auth import token_required
from flaskr.database import db
from flaskr.models import Chat, chats

bp = Blueprint("chat_endpoints", __name__, url_prefix="/chats")

@bp.route('/', methods=['GET'])
@token_required
def get_chats(current_user):
    # Get all chats where user_id == current_user.id
    all_chats = Chat.query.filter(Chat.user_id == current_user.id).all()
    response = []
    for chat in all_chats:
        response.append(chat.get_info())
    return jsonify(response)

#
# @bp.route('/chats/<chat_id>/messages', methods=['GET'])
# @token_required
# def get_messages(current_user, chat_id):
#     #
#     return
#
# @bp.route('/chats/create_chat', methods=['POST'])
# @token_required
# def create_chat(current_user):
#     data = request.get_json()
#     chat = Chat(user_id=current_user.id, company_id=data['company_id'])
#     db.session.add(chat)
#     db.session.commit()
#     return jsonify(chat.get_info())
#

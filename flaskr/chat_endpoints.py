from flask import jsonify, Blueprint, request, make_response

from flaskr.auth import token_required
from flaskr.database import db
from flaskr.models import Chat, chats, User

bp = Blueprint("chat_endpoints", __name__, url_prefix="/chats")

@bp.route('/', methods=['GET'])
@token_required
def get_chats(current_user):
    # Get all chats where user_id == current_user.id
    all_chats = User.query.filter_by(id=current_user.id).first().chats
    response = []
    for chat in all_chats:
        # Find all users who have chat with id = chat_id
        users = User.query.filter(User.chats.any(id=chat.id)).all()
        # Find user who is not current_user
        ava_url = users[0].ava_url if users[0].id != current_user.id else users[1].ava_url if len(users) > 1 else current_user.ava_url
        chat_name = users[0].first_name + ' ' + users[0].last_name if users[0].id != current_user.id else users[1].first_name + ' ' + users[1].last_name if len(users) > 1 else 'Me'
        response.append({
            'id': chat.id,
            'chat_name': chat_name,
            'ava_url': ava_url
        })
    return jsonify(response)


@bp.route('/<chat_id>/messages', methods=['GET'])
@token_required
def get_messages(current_user, chat_id):
    chat = User.query.filter_by(id=current_user.id).first().chats.filter_by(id=chat_id).first()
    if not chat:
        return jsonify({'message': 'No chat found!'})
    messages = chat.messages
    response = []
    for message in messages:
        response.append(message.get_info())
    return jsonify(response)

@bp.route('/create_chat', methods=['POST'])
@token_required
def create_chat(current_user):
    data = request.get_json()
    chat = Chat()

    user_1 = User.query.filter_by(id=current_user.id).first()
    user_1.chats.append(chat)

    user_2 = User.query.filter_by(id=data['user_id']).first()
    user_2.chats.append(chat)

    db.session.add(chat)
    db.session.commit()

    return jsonify(chat.get_info())


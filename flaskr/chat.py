import json
import os

from flask_socketio import send, join_room, leave_room
import jwt

from flaskr.database import db
from flaskr.models import Chat, Message, User
from flaskr.socketio import socketio


def add_message_to_db(chat_name, data):
    chat = Chat.query.filter_by(name=data[chat_name]).first()
    if not chat:
        chat = Chat(name=data[chat_name])
        db.session.add(chat)
        db.session.commit()
    else:
        chat = Chat.query.filter_by(name=data["chat-id"]).first()
        messages = Message.query.filter_by(chat_id=chat.id).all()
        messages.append(Message(text=data['message'], user_id=data['sender-id'], chat_id=chat.id))
        db.session.commit()

    return


def auth_user(f):
    def wrapped(token, *args, **kwargs):
        print('token: ', token)

        if not token:
            send('Token is missing!')
            return
        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            user = User.query.filter_by(id=data['public_id']).first()
        except:
            send('Token is invalid!')
            return

        f(user, *args, **kwargs)

    return wrapped


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on_error_default
def default_error_handler(e):
    print("An error occurred:", e)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


# {
#     "chat-id": 1,
#     "sender-id": 1,
# }
@socketio.on('join chat')
@auth_user
def handle_join_room(user, data):
    # data to be json
    data = json.loads(data)

    print('Received join room request: ', data["chat-id"], data["sender-id"])

    join_room(data["chat-id"])

    send(f'User {data["sender-id"]} joined to room {data["chat-id"]}', room=data["chat-id"])


@socketio.on('leave chat')
@auth_user
def handle_leave_room(user, data):
    # data to be json
    data = json.loads(data)

    print('Received leave room request: ', data["chat-id"], data["sender-id"])

    leave_room(data["chat-id"])

    send(f'User {data["sender-id"]} left room {data["chat-id"]}', room=data["chat-id"], broadcast=True)


@socketio.on('chat message')
@auth_user
def handle_chat_message(user, data):
    # data to be json
    data = json.loads(data)

    add_message_to_db(data["chat-id"], data)

    print('Received chat message: ', data["chat-id"], data["sender-id"], data["message"])

    send(data, room=data["chat-id"], broadcast=True)

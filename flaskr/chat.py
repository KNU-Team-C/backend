from flask_socketio import send

from flaskr.socketio import socketio


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('chat message')
def handle_message(message):
    print('Received message: ' + message)
    send('Hello from the server!', broadcast=True)

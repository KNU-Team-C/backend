from flaskr import app
from flaskr import socketio

if __name__ == '__main__':
    socketio.run(app)
from flask import Flask
from flask_socketio import SocketIO

# create Flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app, debug=True)

@socketio.on('connect')
def test_connection():
    print("connected")

@socketio.on('stroke')
def handle_stroke(json):
    print("received json: " + str(json))
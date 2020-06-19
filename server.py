from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# create Flask object
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('connect')
def on_connect():
    print("connected to websocket")

@socketio.on('disconnect')
def on_disconnect():
    print("disconnected from websocket")

@socketio.on('send-stroke')
def handle_stroke(json):
    print("received json: " + str(json))
    emit('receive-update', "myBoard")

if __name__ == "__main__":
    socketio.run(app, port=8080, debug=True)

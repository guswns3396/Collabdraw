import threading
from flask import Flask
from flask_socketio import SocketIO, emit

# constants
PORT = 8080
HEIGHT = 690
WIDTH = 1280

# create Flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

# server class
class Server:
    def __init__(self, height, width):
        self.board = [[0]*width]*height
        self.lock = threading.Lock()
# instantiate server class for board state
server = Server(HEIGHT,WIDTH)

@socketio.on('connect')
def on_connect():
    print("connected to websocket")
    # broadcast board upon initial connect
    emit('broadcast-board', server.board)

@socketio.on('disconnect')
def on_disconnect():
    print("disconnected from websocket")

@socketio.on('send-stroke')
def handle_stroke(boardJSON):
    # strokeJSON -> list
    print("received json: " + str(boardJSON))
    # lock board
    server.lock.acquire()
    # process stroke & update board
    for pixel in boardJSON:
        # process the whole board (not just stroke)
        pass
    # unlock board
    server.lock.release()
    # broadcast board
    emit('broadcast-board', server.board)

if __name__ == "__main__":
    socketio.run(app, port=PORT, debug=True)

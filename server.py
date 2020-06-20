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
        self.board = []
        for i in range(0,height):
            row = []
            for j in range(0,width):
                row.append(0)
            self.board.append(row)
server = Server(HEIGHT,WIDTH)

@socketio.on('connect')
def on_connect():
    print("connected to websocket")
    emit('receive-update', server.board)

@socketio.on('disconnect')
def on_disconnect():
    print("disconnected from websocket")

@socketio.on('send-stroke')
def handle_stroke(json):
    print(type(json))
    print("received json: " + str(json))
    for pixel in json:
        x = pixel[0]
        y = pixel[1]
        server.board[y][x] = 1
    emit('receive-update', server.board)

if __name__ == "__main__":
    socketio.run(app, port=PORT, debug=True)

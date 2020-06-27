import threading
from flask import Flask
from flask_socketio import SocketIO, emit
from canvas_board import CanvasBoard

# constants
PORT = 8080
HEIGHT = 500
WIDTH = 500

# create Flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

# server class
class Server:
    def __init__(self, imagedata):
        self.board = CanvasBoard(imagedata)
        self.lock = threading.Lock()
    def updateBoard(self,imagedata):
        self.board = CanvasBoard(imagedata)
# instantiate server class for board state
imagedata = {
    'width': WIDTH,
    'height': HEIGHT,
    'data': [0 for i in range(4 * WIDTH * HEIGHT)]
}
server = Server(imagedata)

@socketio.on('connect')
def on_connect():
    print("connected to websocket")

@socketio.on('disconnect')
def on_disconnect():
    print("disconnected from websocket")

if __name__ == "__main__":
    socketio.run(app, port=PORT, debug=True)

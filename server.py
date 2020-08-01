import threading
from flask import Flask
from flask_socketio import SocketIO, emit
from canvas_board import CanvasBoard, CanvasBoardEncoder

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
    def updateBoard(self, diff: dict):
        self.lock.acquire()
        self.board.updateBoard(diff['coord'], diff['val'])
        self.lock.release()

# instantiate server class for board state
imagedata = {
    'width': WIDTH,
    'height': HEIGHT,
    'data': [0 for i in range(4 * WIDTH * HEIGHT)]
}
server = Server(imagedata)

@socketio.on('connect', namespace='/canvas')
def connect_canvas():
    # broadcast board upon initial connect at /canvas endpoint
    # turn board into JSON
    board = CanvasBoardEncoder().encode(server.board)
    emit('broadcast-board', board)

@socketio.on('disconnect')
def on_disconnect():
    print("disconnected from websocket")

@socketio.on('send-stroke', namespace="/canvas")
def handle_send_stroke(diff):
    # diff -> dict
    server.updateBoard(diff)
    # turn board into JSON
    board = CanvasBoardEncoder().encode(server.board)
    emit('broadcast-board', board, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, port=PORT, debug=True)

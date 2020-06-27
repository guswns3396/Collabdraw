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

@app.route('/canvas')
def connect():
    # broadcast board upon initial connect at /canvas endpoint
    emit('broadcast-board', server.board)

@socketio.on('connect')
def on_connect():
    print("connected to websocket")

@socketio.on('disconnect')
def on_disconnect():
    print("disconnected from websocket")

@socketio.on('send-stroke')
def handle_stroke(snapshot):
    # snapshot -> JSON of imagedata
    print("received json: " + str(snapshot))
    # lock board
    server.lock.acquire()
    # update board
    server.updateBoard(snapshot)
    # unlock board
    server.lock.release()
    # broadcast board
    # TODO: send board back as imagedata (perhaps implement server function?)
    emit('broadcast-board', server.board)

if __name__ == "__main__":
    socketio.run(app, port=PORT, debug=True)

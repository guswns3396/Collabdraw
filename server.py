import threading
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
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

    def update_board(self, diffs: list):
        self.lock.acquire()
        self.board.update_board(diffs)
        self.lock.release()


# instantiate server class for board state
imagedata = {
    'width': WIDTH,
    'height': HEIGHT,
    'data': [0 for i in range(4 * WIDTH * HEIGHT)]
}
server = Server(imagedata)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@socketio.on('connect', namespace='/canvas')
def connect_canvas():
    # broadcast board upon initial connect at /canvas endpoint
    # turn board into JSON
    board = CanvasBoardEncoder().encode(server.board)
    emit('initialize-board', board)

@socketio.on('disconnect')
def on_disconnect():
    print("disconnected from websocket")

@socketio.on('send-stroke', namespace="/canvas")
def handle_send_stroke(stroke):
    server.update_board(stroke['diffs'])
    # broadcast the new change
    emit('broadcast-stroke', stroke, broadcast=True)

@socketio.on('join')
def on_join(room_data):
    room = room_data['room_id']
    join_room(room)
    msg = 'A client has joined the room'
    emit('client-join', msg, room=room)
    board = CanvasBoardEncoder().encode(server.board)
    emit('broadcast-board', board)

@socketio.on('leave')
def on_leave(room_data):
    room = room_data['id']
    leave_room(room)
    msg = 'A client has left the room'
    emit('client-leave', msg, room=room)

if __name__ == "__main__":
    # TODO(hyunbumy): Modify the host to restrict the access from the frontend
    # served by the same production server.
    socketio.run(app, port=PORT, debug=True, host='0.0.0.0')

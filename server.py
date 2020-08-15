from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from canvas_board import CanvasBoard, CanvasBoardEncoder

# constants
PORT = 8080
HEIGHT = 500
WIDTH = 500

# create Flask object
app = Flask(__name__, template_folder='static/', static_folder='static/')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

# server class
class Server:
    def __init__(self, boards):
        """
        :param boards: dict that maps room id to CanvasBoard
        """
        self.boards = boards

    def update_board(self, diffs: list, room_id: str):
        self.boards[room_id].update_board(diffs)

# instantiate server class for board state
imagedata = {
    'width': WIDTH,
    'height': HEIGHT,
    'data': [0 for i in range(4 * WIDTH * HEIGHT)]
}
server = Server({})

rooms = []

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/create')
def create():
    # TODO: Make random room id & check if valid
    room = 'TestRoom'
    rooms.append(room)
    response = jsonify(room_id=room)
    # just return response with room id
    # don't worry about frontend
    return response

@socketio.on('connect', namespace='/canvas')
def connect_canvas():
    print("connected to websocket")

@socketio.on('disconnect')
def on_disconnect():
    print("disconnected from websocket")

@socketio.on('send-stroke', namespace="/canvas")
def handle_send_stroke(stroke, room_data):
    room_id = room_data['room_id']
    if room_id in server.boards:
        server.update_board(stroke['diffs'], room_id)
        emit('broadcast-stroke', stroke, broadcast=True, room=room_id)
    else:
        print("Error: no room found")

@socketio.on('join', namespace='/canvas')
def on_join(room_data):
    room_id = room_data['room_id']
    # instantiate initial CanvasBoard
    if room_id not in server.boards:
        server.boards[room_id] = CanvasBoard(imagedata)
    join_room(room_id)
    msg = 'A client has joined the room'
    print(msg, room_id)
    board = CanvasBoardEncoder().encode(server.boards[room_id])
    emit('initialize-board', board, room=room_id)

if __name__ == "__main__":
    # TODO(hyunbumy): Modify the host to restrict the access from the frontend
    # served by the same production server.
    socketio.run(app, port=PORT, debug=True, host='0.0.0.0')

from flask import Flask, jsonify, abort, Response
from flask_socketio import SocketIO, emit, join_room, leave_room
from canvas_board import CanvasBoard, WIDTH, HEIGHT

# constants
PORT = 8080

# create Flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

# server class
class Server:
    def __init__(self):
        self.__boards = {}

    def get_ids(self):
        return self.__boards.keys()

    def add_board(self, room_id, board):
        if room_id in self.__boards:
            assert ValueError('Room with given ID already exists')
        else:
            self.__boards[room_id] = board

    def get_board(self, room_id):
        return self.__boards[room_id]

    def update_board(self, diffs: list, room_id: str):
        if room_id not in self.__boards:
            assert ValueError('Room with given ID does not exist')
        else:
            self.__boards[room_id].update_board(diffs)

server = Server()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/create')
def create_room(payload):
    room = payload['room_id']
    if room in server.get_ids():
        abort(Response('Room with given ID already exists'))
    server.add_board(room, CanvasBoard.create_board(WIDTH, HEIGHT))
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
def handle_send_stroke(payload):
    room_id = payload['room_id']
    if room_id in server.get_ids():
        server.update_board(payload['diffs'], room_id)
        emit('broadcast-stroke', payload['diffs'], room=room_id)
    else:
        print("Error: no room found")
        abort(Response('Room with given ID does not exist'))

@socketio.on('join', namespace='/canvas')
def on_join(payload):
    room_id = payload['room_id']
    if room_id not in server.get_ids():
        abort(Response('Room with given ID does not exist'))
    join_room(room_id)
    print('A client has joined the room', room_id)
    emit('initialize-board', {'board': server.get_board(room_id).to_dict()})

if __name__ == "__main__":
    # TODO(hyunbumy): Modify the host to restrict the access from the frontend
    # served by the same production server.
    socketio.run(app, port=PORT, debug=True, host='0.0.0.0')

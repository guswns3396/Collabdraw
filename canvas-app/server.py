from flask import Flask, jsonify, abort, Response
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
from canvas_board import CanvasBoard, WIDTH, HEIGHT
from room import Room

# constants
PORT = 8080

# create Flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

# server class
class Server:
    def __init__(self):
        # TODO(guswns3396): implement Room class; replace boards with rooms
        self.__rooms = {}

    def get_rooms(self):
        return self.__rooms.keys()

    def add_room(self, room_id, room):
        if room_id in self.get_rooms():
            raise ValueError('Room with given ID already exists')
        else:
            self.__rooms[room_id] = room

    def get_room(self, room_id):
        if room_id in self.get_rooms():
            return self.__rooms[room_id]
        else:
            raise ValueError('Room with given ID does not exist')

    def update_room_board(self, diffs: list, room_id: str):
        if room_id not in self.get_rooms():
            raise ValueError('Room with given ID does not exist')
        else:
            self.__rooms[room_id].get_board().update_board(diffs)

    def delete_room(self, room_id):
        if room_id in self.get_rooms():
            del self.__rooms[room_id]
        else:
            raise ValueError('Room with given ID does not exist')

server = Server()

@app.route('/create/<room_id>')
def create_room(room_id):
    try:
        server.add_room(room_id, CanvasBoard.create_board(WIDTH, HEIGHT))
    except:
        abort(Response('Room with given ID already exists', status=400))
    response = jsonify(room_id=room_id)
    response.headers.add('Access-Control-Allow-Origin', '*')
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
    try:
        server.update_room_board(payload['diffs'], room_id)
    except:
        print("Error: no room found")
        emit('invalid-room', 'Room with given ID not found')
    else:
        emit('broadcast-stroke', {'diffs': payload['diffs']}, room=room_id)

@socketio.on('join', namespace='/canvas')
def on_join(payload):
    room_id = payload['room_id']
    if room_id not in server.get_rooms():
        emit('invalid-room', 'Room with given ID not found')
    join_room(room_id)
    server.get_room(room_id).decrement()
    print('A client has joined the room', room_id)
    emit('initialize-board', {'board': server.get_room(room_id).get_board().to_dict()})

@socketio.on('leave', namespace='canvas')
def on_leave(payload):
    room_id = payload['room_id']
    if room_id not in server.get_rooms():
        emit('invalid-room', 'Room with given ID not found')
    leave_room(room_id)
    server.get_room(room_id).decrement()
    print('A client has left the room', room_id)
    # TODO(guswns3396): check number of users, purge when last one leaves
    if server.get_room(room_id).get_headcount() == 0:
        close_room(room_id)
        server.delete_room(room_id)

if __name__ == "__main__":
    # TODO(hyunbumy): Modify the host to restrict the access from the frontend
    # served by the same production server.
    socketio.run(app, port=PORT, debug=True, host='0.0.0.0')

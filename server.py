import unittest

from flask import Flask
from flask_socketio import SocketIO, emit

# create Flask object
app = Flask(__name__,template_folder='./static',static_folder='./static')
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


class TestSocketIO(unittest.TestCase):
    def test_connect(self):
        client1 = socketio.test_client(app)
        client2 = socketio.test_client(app)
        self.assertTrue(client1.is_connected())
        self.assertTrue(client2.is_connected())
        self.assertNotEqual(client1.sid, client2.sid)
        client1.disconnect()
        self.assertFalse(client1.is_connected())
        self.assertTrue(client2.is_connected())
        client2.disconnect()
        self.assertFalse(client2.is_connected())

    def test_stroke(self):
        client = socketio.test_client(app)
        client.emit('send-stroke', 'myStroke')
        received_data = client.get_received()
        myData = received_data[0]['args'][0]
        self.assertEqual(myData, "myBoard")


if __name__ == '__main__':
    unittest.main()
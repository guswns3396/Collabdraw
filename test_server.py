import unittest
from unittest.mock import patch
import io
import server
import json

class TestSocketIOConnection(unittest.TestCase):
    def test_disconnect_printsDisconnectionMessage(self):
        client = server.socketio.test_client(server.app)
        expectedOutput = "disconnected from websocket\n"

        with patch('sys.stdout', new=io.StringIO()) as myOutput:
            client.disconnect()

            self.assertEqual(myOutput.getvalue(), expectedOutput)

    def test_connect_canvas_printsConnectionMessage(self):
        expectedOutput = "connected to websocket\n"
        client = server.socketio.test_client(server.app)

        with patch('sys.stdout', new=io.StringIO()) as myOutput:
            client.connect('/canvas')
            output = myOutput.getvalue()

        self.assertEqual(expectedOutput, output)

class TestOnJoin(unittest.TestCase):
    def initializesBoard(self):
        client1 = server.socketio.test_client(server.app)
        client1.connect('/canvas')
        room_data = {'room_id': 'myTestRoom'}
        client1.emit('join', room_data, namespace='/canvas')
        diffs = {'diffs': [{'coord': 0, 'val': 100}]}
        client1.emit('send-stroke', diffs, room_data, namespace='/canvas')
        client2 = server.socketio.test_client(server.app)
        client2.connect('/canvas')

        client2.emit('join', room_data, namespace='/canvas')

        received_data = client2.get_received('/canvas')
        board = None
        for data in received_data:
            if data['name'] == 'initialize-board':
                board = json.loads(data['args'][0])['data']
        self.assertEqual(100, board[0])

    def test_on_join_keepsBoardsSeparateForEachRoom(self):
        client1 = server.socketio.test_client(server.app)
        client1.connect('/canvas')
        room_data1 = {'room_id': 'room1'}
        client1.emit('join', room_data1, namespace='/canvas')
        diffs = {'diffs': [{'coord': 0, 'val': 100}]}
        client1.emit('send-stroke', diffs, room_data1, namespace='/canvas')
        client2 = server.socketio.test_client(server.app)
        client2.connect('/canvas')
        room_data2 = {'room_id': 'room2'}

        client2.emit('join', room_data2, namespace='/canvas')

        board1 = None
        board2 = None
        received_data = client1.get_received('/canvas')
        for data in received_data:
            if data['name'] == 'initialize-board':
                board1 = json.loads(data['args'][0])['data']
        received_data = client2.get_received('/canvas')
        for data in received_data:
            if data['name'] == 'initialize-board':
                board2 = json.loads(data['args'][0])['data']
        self.assertNotEqual(board1, board2)

class TestSendStroke(unittest.TestCase):
    def printsErrorMessageIfNoRoomFound(self):
        pass

    def updatesBoardState(self):
        client = server.socketio.test_client(server.app)
        client.connect('/canvas')
        diffs = {'diffs': [{'coord': 0, 'val': 100}]}
        room_data = {'room_id': 'myTestRoom'}

        client.emit('send-stroke', diffs, room_data, namespace='/canvas')


        self.assertEqual(server.server.boards.data[0], 100)

    def boardcastsDiffs(self):
        client1 = server.socketio.test_client(server.app)
        client1.connect('/canvas')
        client2 = server.socketio.test_client(server.app)
        client2.connect('/canvas')
        stroke = {'diffs': [{'coord': 0, 'val': 100}]}

        client1.emit('send-stroke', stroke, namespace='/canvas')

        received = client2.get_received('/canvas')
        self.assertIn({
            'name': 'broadcast-stroke',
            'args': [stroke],
            'namespace': '/canvas'
        }, received)

if __name__ == '__main__':
    unittest.main()

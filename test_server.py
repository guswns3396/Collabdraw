import unittest
from unittest.mock import patch
import io
import server
import json

class TestSocketIOConnection(unittest.TestCase):
    def test_printsDisconnectionMessage(self):
        client = server.socketio.test_client(server.app)
        expectedOutput = "disconnected from websocket\n"

        with patch('sys.stdout', new=io.StringIO()) as myOutput:
            client.disconnect()

            self.assertEqual(myOutput.getvalue(), expectedOutput)

    def test_printsConnectionMessage(self):
        expectedOutput = "connected to websocket\n"
        client = server.socketio.test_client(server.app)

        with patch('sys.stdout', new=io.StringIO()) as myOutput:
            client.connect('/canvas')
            output = myOutput.getvalue()

        self.assertEqual(expectedOutput, output)

class TestOnJoin(unittest.TestCase):
    def test_initializesBoardForNewClient(self):
        client1 = server.socketio.test_client(server.app)
        client1.connect('/canvas')
        room_data = {'room_id': 'myTestRoom'}
        client1.emit('join', room_data, namespace='/canvas')
        stroke = {'diffs': [{'coord': 0, 'val': 100}]}
        server.server.update_board(stroke['diffs'], room_data['room_id'])
        client2 = server.socketio.test_client(server.app)
        client2.connect('/canvas')

        client2.emit('join', room_data, namespace='/canvas')

        received_data = client2.get_received('/canvas')
        board = None
        for data in received_data:
            if data['name'] == 'initialize-board':
                board = json.loads(data['args'][0])['data']
        self.assertEqual(100, board[0])

    def test_keepsBoardsSeparateForEachRoom(self):
        client1 = server.socketio.test_client(server.app)
        client1.connect('/canvas')
        room_data1 = {'room_id': 'room1'}
        client1.emit('join', room_data1, namespace='/canvas')
        stroke = {'diffs': [{'coord': 0, 'val': 100}]}
        server.server.update_board(stroke['diffs'], room_data1['room_id'])
        client2 = server.socketio.test_client(server.app)
        client2.connect('/canvas')
        room_data2 = {'room_id': 'room2'}

        client2.emit('join', room_data2, namespace='/canvas')

        board1 = server.server.boards[room_data1['room_id']].data
        board2 = None
        received_data = client2.get_received('/canvas')
        for data in received_data:
            if data['name'] == 'initialize-board':
                board2 = json.loads(data['args'][0])['data']
        self.assertNotEqual(board1[0], board2[0])

class TestSendStroke(unittest.TestCase):
    def test_printsErrorMessageIfNoRoomFound(self):
        client = server.socketio.test_client(server.app)
        client.connect('/canvas')
        stroke = {}
        room_data = {'room_id': 'test'}

        with patch('sys.stdout', new=io.StringIO()) as myOutput:
            client.emit('send-stroke', stroke, room_data, namespace='/canvas')
            output = myOutput.getvalue()

        expected = "Error: no room found\n"
        self.assertEqual(expected, output)

    def test_updatesBoardStateByRoom(self):
        client1 = server.socketio.test_client(server.app)
        client2 = server.socketio.test_client(server.app)
        client1.connect('/canvas')
        client2.connect('/canvas')
        room_data1 = {'room_id': 'room1'}
        room_data2 = {'room_id': 'room2'}
        client1.emit('join', room_data1, namespace='/canvas')
        client2.emit('join', room_data2, namespace='/canvas')
        diffs = {'diffs': [{'coord': 0, 'val': 100}]}

        client1.emit('send-stroke', diffs, room_data1, namespace='/canvas')

        board1 = server.server.boards[room_data1['room_id']].data
        board2 = server.server.boards[room_data2['room_id']].data
        self.assertTrue(board1[0] == 100, board2[0] == 0)

    def test_boardcastsDiffs(self):
        room_data = {'room_id': 'room1'}
        client1 = server.socketio.test_client(server.app)
        client1.connect('/canvas')
        client1.emit('join', room_data, namespace='/canvas')
        client2 = server.socketio.test_client(server.app)
        client2.connect('/canvas')
        client2.emit('join', room_data, namespace='/canvas')
        stroke = {'diffs': [{'coord': 0, 'val': 100}]}

        client1.emit('send-stroke', stroke, room_data, namespace='/canvas')

        received = client2.get_received('/canvas')
        self.assertIn({
            'name': 'broadcast-stroke',
            'args': [stroke],
            'namespace': '/canvas'
        }, received)

class TestCreate(unittest.TestCase):
    def test_createsID(self):
        server.app.testing = True
        client = server.app.test_client()

        response = client.get('/create')

        room_data = response.get_json()
        id = room_data['room_id']
        self.assertTrue(id is not None)

    def test_skipsDuplicate(self):
        server.app.testing = True
        client1 = server.app.test_client()
        client2 = server.app.test_client()
        server.random.seed(0)
        response1 = client1.get('/create')
        room_data1 = response1.get_json()
        id1 = room_data1['room_id']
        server.server.boards[id1] = None
        server.random.seed(0)

        response2 = client2.get('/create')

        room_data2 = response2.get_json()
        id2 = room_data2['room_id']
        self.assertNotEqual(id1, id2)

if __name__ == '__main__':
    unittest.main()

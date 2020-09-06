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
        server.server.add_board('testid', server.CanvasBoard.create_board(server.WIDTH, server.HEIGHT))
        client1 = server.socketio.test_client(server.app)
        client1.connect('/canvas')
        room_data = {'room_id': 'testid'}
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
                board = data['args'][0]['board']['data']
        self.assertEqual(100, board[0])

    def test_keepsBoardsSeparateForEachRoom(self):
        server.server.add_board('room1', server.CanvasBoard.create_board(server.WIDTH, server.HEIGHT))
        server.server.add_board('room2', server.CanvasBoard.create_board(server.WIDTH, server.HEIGHT))
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

        board1 = server.server.get_board(room_data1['room_id']).data
        board2 = None
        received_data = client2.get_received('/canvas')
        for data in received_data:
            if data['name'] == 'initialize-board':
                board2 = data['args'][0]['board']['data']
        self.assertNotEqual(board1[0], board2[0])

class TestSendStroke(unittest.TestCase):
    def test_errorIfNoRoomFound(self):
        server.server.add_board('testroom', server.CanvasBoard.create_board(server.WIDTH, server.HEIGHT))
        client = server.socketio.test_client(server.app)
        client.connect('/canvas')
        payload = {'diffs': {}, 'room_id': 'test'}

        client.emit('send-stroke', payload, namespace='/canvas')

        received = client.get_received('/canvas')
        self.assertIn({
            'name': 'invalid-room',
            'args': ['Room with given ID not found'],
            'namespace': '/canvas'
        }, received)

    def test_updatesBoardStateByRoom(self):
        server.server.add_board('room1', server.CanvasBoard.create_board(server.WIDTH, server.HEIGHT))
        server.server.add_board('room2', server.CanvasBoard.create_board(server.WIDTH, server.HEIGHT))
        client1 = server.socketio.test_client(server.app)
        client2 = server.socketio.test_client(server.app)
        client1.connect('/canvas')
        client2.connect('/canvas')
        room_data1 = {'room_id': 'room1'}
        room_data2 = {'room_id': 'room2'}
        client1.emit('join', room_data1, namespace='/canvas')
        client2.emit('join', room_data2, namespace='/canvas')
        payload = {'diffs': [{'coord': 0, 'val': 100}], 'room_id': 'room1'}

        client1.emit('send-stroke', payload, namespace='/canvas')

        board1 = server.server.get_board(room_data1['room_id']).data
        board2 = server.server.get_board(room_data2['room_id']).data
        self.assertTrue(board1[0] == 100, board2[0] == 0)

    def test_boardcastsDiffs(self):
        server.server.add_board('room1', server.CanvasBoard.create_board(server.WIDTH, server.HEIGHT))
        room_data = {'room_id': 'room1'}
        client1 = server.socketio.test_client(server.app)
        client1.connect('/canvas')
        client1.emit('join', room_data, namespace='/canvas')
        client2 = server.socketio.test_client(server.app)
        client2.connect('/canvas')
        client2.emit('join', room_data, namespace='/canvas')
        payload = {'diffs': [{'coord': 0, 'val': 100}], 'room_id': 'room1'}

        client1.emit('send-stroke', payload, namespace='/canvas')

        received = client2.get_received('/canvas')
        self.assertIn({
            'name': 'broadcast-stroke',
            'args': [payload['diffs']],
            'namespace': '/canvas'
        }, received)

class TestCreate(unittest.TestCase):
    def test_createsID(self):
        server.app.testing = True
        client = server.app.test_client()

        response = client.get('/create/testID')

        room_data = response.get_json()
        id = room_data['room_id']
        self.assertTrue(id == 'testID')

    def test_errorIfDuplicate(self):
        server.app.testing = True
        client1 = server.app.test_client()
        client2 = server.app.test_client()
        client1.get('/create/test1')

        response2 = client2.get('/create/test1')

        self.assertEqual(400, response2.status_code)

if __name__ == '__main__':
    unittest.main()

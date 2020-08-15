import unittest
from unittest.mock import patch
import io
import server


class TestSocketIO(unittest.TestCase):
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

    def test_sendStroke_updatesBoardState(self):
        client = server.socketio.test_client(server.app)
        client.connect('/canvas')
        diffs = {'diffs': [{'coord': 0, 'val': 100}]}

        client.emit('send-stroke', diffs, namespace='/canvas')

        self.assertEqual(server.server.board.data[0], 100)

    def test_sendStroke_boardcastsDiffs(self):
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

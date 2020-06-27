import unittest
from unittest.mock import patch
import io
import sys
import server

class TestSocketIO(unittest.TestCase):
    def test_connect_emitsBoardState(self):
        client = server.socketio.test_client(server.app)
        HEIGHT = 500
        WIDTH = 500

        received_data = client.get_received()

        self.assertEqual(received_data[0]['args'][0],[[0]*WIDTH]*HEIGHT)

    def test_disconnect_printsDisconnectionMessage(self):
        client = server.socketio.test_client(server.app)
        expectedOutput = "disconnected from websocket\n"

        with patch('sys.stdout', new=io.StringIO()) as myOutput:
            client.disconnect()

            self.assertEqual(myOutput.getvalue(), expectedOutput)

    def test_if_clients_have_different_ids(self):
        client1 = server.socketio.test_client(server.app)
        client2 = server.socketio.test_client(server.app)

        self.assertNotEqual(client1.sid, client2.sid)

    def test_stroke_communication_between_server_and_client(self):
        client = server.socketio.test_client(server.app)

        client.emit('send-stroke', 'myStroke')
        received_data = client.get_received()
        myData = received_data[0]['args'][0]

        self.assertEqual(myData, "myBoard")

if __name__ == '__main__':
    unittest.main()

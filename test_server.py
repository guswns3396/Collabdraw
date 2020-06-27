import unittest
from unittest.mock import patch
import io
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

if __name__ == '__main__':
    unittest.main()

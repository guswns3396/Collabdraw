import unittest
from unittest.mock import patch
import io
import server

class TestSocketIO(unittest.TestCase):

    def test_connect_printsConnectionMessage(self):
        expectedOutput = "connected to websocket\n"

        with patch('sys.stdout', new=io.StringIO()) as myOutput:
            client = server.socketio.test_client(server.app)

            self.assertEqual(myOutput.getvalue(), expectedOutput)

    def test_disconnect_printsDisconnectionMessage(self):
        client = server.socketio.test_client(server.app)
        expectedOutput = "disconnected from websocket\n"

        with patch('sys.stdout', new=io.StringIO()) as myOutput:
            client.disconnect()

            self.assertEqual(myOutput.getvalue(), expectedOutput)

    def test_connect_canvas_emitsBoardAsJSON(self):
        client = server.socketio.test_client(server.app)
        server_expected = server.server.board

        client.connect('/canvas')

        received_data = client.get_received('/canvas')
        server_output = received_data[0]['args'][0]
        self.assertEqual(server_expected,server_output)




if __name__ == '__main__':
    unittest.main()

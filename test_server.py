import unittest
from unittest.mock import patch
import io
import server

class TestSocketIO(unittest.TestCase):
    def test_connect_canvas_emitsBoard(self):
        pass

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

    def test_handle_stroke_receivesSnapshot(self):
        pass

    def test_handle_stroke_updatesBoard(self):
        pass

    def test_handle_stroke_emitsBoard(self):
        pass

if __name__ == '__main__':
    unittest.main()

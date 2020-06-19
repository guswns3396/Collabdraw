import unittest
import server

class TestSocketIO(unittest.TestCase):
    def test_if_connection_successful(self):
        # arrange & act
        client = server.socketio.test_client(server.app)
        # assert
        self.assertTrue(client.is_connected())

    def test_if_disconnection_successful(self):
        # arrange
        client = server.socketio.test_client(server.app)
        # act
        client.disconnect()
        # assert
        self.assertFalse(client.is_connected())

    def test_if_clients_have_different_ids(self):
        # arrange & act
        client1 = server.socketio.test_client(server.app)
        client2 = server.socketio.test_client(server.app)
        # assert
        self.assertNotEqual(client1.sid, client2.sid)

    def test_stroke_communication_between_server_and_client(self):
        # arrange
        client = server.socketio.test_client(server.app)
        # act
        client.emit('send-stroke', 'myStroke')
        received_data = client.get_received()
        myData = received_data[0]['args'][0]
        # assert
        self.assertEqual(myData, "myBoard")

if __name__ == '__main__':
    unittest.main()

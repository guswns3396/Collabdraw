import unittest
import server

class TestSocketIO(unittest.TestCase):
    def test_connect(self):
        client1 = server.socketio.test_client(server.app)
        client2 = server.socketio.test_client(server.app)
        self.assertTrue(client1.is_connected())
        self.assertTrue(client2.is_connected())
        self.assertNotEqual(client1.sid, client2.sid)
        client1.disconnect()
        self.assertFalse(client1.is_connected())
        self.assertTrue(client2.is_connected())
        client2.disconnect()
        self.assertFalse(client2.is_connected())

    def test_stroke(self):
        client = server.socketio.test_client(server.app)
        client.emit('send-stroke', 'myStroke')
        received_data = client.get_received()
        myData = received_data[0]['args'][0]
        self.assertEqual(myData, "myBoard")

if __name__ == '__main__':
    unittest.main()
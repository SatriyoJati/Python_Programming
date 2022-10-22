import paho.mqtt.client as mqtt
import time

class TestBrokerConnection(unittest.TestCase):
    def setUp(self):
        self.client = mqtt.Client("Test Oxy Client")
        self.client.on_connect = self.on_connect
        self.broker = "localhost"
        self.port = 1883
        self.has_connected = False

    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            self.has_connected = True

    def test_connection(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        time.sleep(2)
        self.client.loop_end()
        self.assertTrue(self.has_connected)

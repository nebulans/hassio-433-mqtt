import time
import threading

import paho.mqtt.client as mqtt


CONNECT_CODES = {
    0: "Connected",
    1: "Incorrect protocol",
    2: "Invalid client ID",
    3: "Server unavailable",
    4: "Bad username/password",
    5: "Unauthorized"
}


class MQTTConnectionRefused(Exception):
    pass


class MQTTOutput(object):

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.client = mqtt.Client()
        self.client.username_pw_set(user, password)
        self._connect_event = threading.Event()
        self._connect_result = None

    def connect(self):
        # Connect syncronously, raising an exception if the connection fails
        self.client.on_connect = self._on_connect
        self.client.connect(self.host)
        self.client.loop_start()
        self._connect_event.wait()
        if isinstance(self._connect_result, Exception):
            raise self._connect_result

    def publish(self, topic, payload):
        if not self.client.is_connected():
            raise ValueError('Client not connected!')
        print(f'sending to topic "{topic}" wih payload "{payload}"')
        self.client.publish(topic, payload)

    def _on_connect(self, _client, userdata, flags, rc):
        if rc > 0:
            self._connect_result = MQTTConnectionRefused(f'Connection refused, {CONNECT_CODES.get(rc, "Reason unknown")} (rc {rc})')
        else:
            self.connect_result = True
        self._connect_event.set()
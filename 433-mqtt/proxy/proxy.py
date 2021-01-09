import argparse
import queue
import json
import sys
import threading

from .listeners import SubprocessListener
from .rtl433 import RTL433Command
from .output import MQTTOutput


class ProxyApplication(object):

    def __init__(self, config):
        self.config = config
        self.queue = queue.Queue()
        self.outputs = []
        self.listeners = []
        self.processor = threading.Thread(target=self.process, daemon=True)

    def get_outputs(self):
        yield MQTTOutput(self.config['mqtt']['host'], self.config['mqtt']['user'], self.config['mqtt']['password'])

    def get_listeners(self):
        for device in self.config['devices']:
            command = RTL433Command(**device).get_command()
            yield SubprocessListener(command)

    def connect_outputs(self):
        self.outputs = list(self.get_outputs())
        for o in self.outputs:
            o.connect()

    def start_listeners(self):
        self.listeners = list(self.get_listeners())
        threads = [threading.Thread(target=l.read, args=[self.queue], daemon=True) for l in self.listeners]
        for t in threads:
            t.start()

    def enrich(self, item):
        return self.config['mqtt']['topic_base'], item

    def process(self):
        while True:
            item = self.queue.get()
            topic, item = self.enrich(item)
            for o in self.outputs:
                o.publish(topic, item)

    def run(self):
        self.connect_outputs()
        self.start_listeners()
        self.processor.start()


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('config_path')
    args = parser.parse_args(argv)
    with open(args.config_path) as f:
        config = json.load(f)
    application = ProxyApplication(config)
    application.run()


if __name__ == '__main__':
    main(sys.argv[1:])

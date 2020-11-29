import abc
import time
import subprocess


class Listener(abc.ABC):

    @abc.abstractmethod
    def read(self, output_queue):
        pass


class FileListener(Listener):

    def __init__(self, path):
        self.path = path

    def read(self, output_queue):
        with open(self.path) as f:
            while True:
                l = f.readline()
                if l:
                    output_queue.put(l.strip())
                else:
                    time.sleep(0.1)


class SubprocessListener(Listener):

    def __init__(self, command):
        self.command = command

    def get_process(self):
        return subprocess.Popen(self.command, stdout=subprocess.PIPE)

    def read(self, output_queue):
        with self.get_process() as process:
            while True:
                l = process.stdout.readline()
                if l:
                    output_queue.put(l.strip())
                else:
                    time.sleep(0.1)
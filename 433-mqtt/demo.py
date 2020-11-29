from queue import Queue
import sys
from threading import Thread

from proxy.listeners import FileListener, SubprocessListener
from proxy.output import MQTTOutput


def main(args):
    listeners = [SubprocessListener(['tail', '-f', p]) for p in args]
    out_q = Queue()
    threads = [Thread(target=l.read, args=[out_q], daemon=True) for l in listeners]
    for t in threads:
        t.start()
    output = MQTTOutput('192.168.178.2', 'sdr433', 'sdr433')
    output.connect()
    try:
        while True:
            i = out_q.get()
            output.publish('debug/proxy', i)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main(sys.argv[1:])
from pylib import IS_PY2

from time import sleep
import threading
import traceback

from pylib.logger import logger

if IS_PY2:
    import Queue
else:
    import queue as Queue


class ThreadPool(object):
    """Handler with a fixed size pool of threads which process some tasks."""

    def __init__(self, thread_count=10, is_daemon=True):
        self.queue = Queue.Queue()
        self.thread_count = thread_count
        self.is_daemon = is_daemon

    def serveThread(self):
        """"""
        while True:
            try:
                args = self.queue.get()
                self.serve(args)
            except Exception as err:
                error_track = traceback.format_exc()
                errmsg = '%s\n%s' % (err.message, error_track)
                logger.error(errmsg)

    def serve(self, args):
        """ main handler function
        """
        raise NotImplementedError()

    def start(self):
        """ use mulit thread to listen queue
        """
        for i in range(self.thread_count):
            try:
                t = threading.Thread(target=self.serveThread)
                t.setDaemon(self.is_daemon)
                t.start()
            except Exception as err:
                error_track = traceback.format_exc()
                errmsg = '%s\n%s' % (err.message, error_track)
                logger.error(errmsg)

        self.run()

    def run(self):
        """ to produce data and push to the queue
        """
        raise NotImplementedError()


class __Example(ThreadPool):

    def run(self):
        for i in range(10):
            self.queue.put(i)
            sleep(1)

    def serve(self, num):
        logger.info(num)


if __name__ == "__main__":
    ex = __Example()
    ex.start()

#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

__author__ = 'lycheng'
__email__ = "lycheng997@gmail.com"
__date__ = '2014-01-23'

from mylog import logger

from time import sleep
import threading
import traceback
import Queue

class ThreadPool(object):
    """Handler with a fixed size pool of threads which process some tasks."""

    def __init__(self, thread_count=10, is_daemon=True):
        self.queue = Queue.Queue()
        self.thread_count = thread_count
        # 当 daemon 被设置为 True 时，如果主线程退出，那么子线程也将跟着退出
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
        """ 实际的处理函数
        """
        raise NotImplementedError()

    def start(self):
        """ 启动多个线程去监听队列
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
        """ 往队列塞数据的函数
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


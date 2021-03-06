# coding: utf-8

"""
@author: 武明辉 
@time: 2018/5/16 18:40
"""
import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

from utils import time_this

selector = DefaultSelector()
stopped = False
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}


class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)


class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)


class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(('example.com', 80))
        except BlockingIOError:
            pass
        f = Future()

        def on_connected():
            f.set_result(None)

        selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        yield f
        selector.unregister(sock.fileno())
        get = 'GET {0} HTTP/1.0\r\nHOST: example.com\r\n\r\n'.format(self.url)
        sock.send(get.encode())

        global stopped
        while True:
            f = Future()

            def on_readable():
                f.set_result(sock.recv(4086))

            selector.register(sock.fileno(), EVENT_READ, on_readable)
            chunk = yield f
            selector.unregister(sock.fileno())
            if chunk:
                self.response += chunk
            else:
                urls_todo.remove(self.url)
                if not urls_todo:
                    stopped = True
                break


@time_this
def loop():
    while not stopped:
        events = selector.select()
        for key, mask in events:
            call_back = key.data
            call_back(key, mask)


if __name__ == '__main__':
    for url in urls_todo:
        crawler = Crawler(url)
        crawler.fetch()
    loop()

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


class Crawler:
    def __init__(self, url):
        self.url = url
        self.sock = None
        self.response = b''

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('example.com', 80))
        except BlockingIOError:
            pass
        selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        selector.unregister(key.fd)
        get = 'GET {0} HTTP/1.0\r\nHOST: example.com\r\n\r\n'.format(self.url)
        self.sock.send(get.encode())
        selector.register(key.fd, EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped
        chunk = self.sock.recv(4089)
        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd)
            urls_todo.remove(self.url)
            if not urls_todo:
                stopped = True


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

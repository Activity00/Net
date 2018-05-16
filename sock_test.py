import socket
from concurrent import futures

from utils import time_this


def blocking_way():
    s = socket.socket()
    s.connect(('example.com', 80))
    request = b'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n'
    s.send(request)
    chunk = s.recv(4068)
    response = b''
    while chunk:
        response += chunk
        chunk = s.recv(4068)
    return response


def no_blocking_way():
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('example.com', 80))
    except BlockingIOError as e:
        pass

    data = b'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n'
    while True:
        try:
            # 只到不抛异常发送退出
            s.send(data)
            break
        except OSError:
            pass

    response = b''
    while True:
        try:
            chunk = s.recv(4096)
            while chunk:
                response += chunk
                chunk = s.recv(4096)
            break
        except OSError:
            pass

    return response


@time_this
def sync_way_block():
    res = []
    for i in range(10):
        res.append(blocking_way())
    return len(res)


@time_this
def sync_way_no_block():
    res = []
    for i in range(10):
        res.append(no_blocking_way())
    return len(res)


@time_this
def process_way():
    workers = 10
    with futures.ProcessPoolExecutor(workers) as excutor:
        futs = {excutor.submit(blocking_way) for _ in range(10)}
        return len([fut.result() for fut in futs])


@time_this
def thread_way():
    workers = 10
    with futures.ThreadPoolExecutor(workers) as excutor:
        futs = {excutor.submit(blocking_way) for _ in range(10)}
        return len([fut.result() for fut in futs])

if __name__ == '__main__':
    sync_way_no_block()
    process_way()
    thread_way()

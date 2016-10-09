#-*- coding: utf-8 -*-
'''
Created on 2016年10月9日

@author: Activity00
'''
from SocketServer import StreamRequestHandler, TCPServer

class MyHandler(StreamRequestHandler):
   
    def handle(self):
        addr=self.request.getpeername()
        print '得到连接来自',addr
        self.wfile.write('这是一个tcp socket server')

host=''
port=1234
server=TCPServer((host,port), MyHandler)
server.serve_forever()





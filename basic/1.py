#-*- coding: utf-8 -*-
'''
Created on 2016年10月9日

@author: Activity00
'''
import socket


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
print host
port=1234
s.bind((host,port))
s.listen(10)  #队列长度

while True:
    c,addr=s.accept()
    print '得到一个连接来自',addr
    c.send('你好，我是一个简单的服务器')
    c.close()




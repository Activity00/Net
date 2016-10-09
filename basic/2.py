#-*- coding: utf-8 -*-
'''
Created on 2016年10月9日

@author: 武明辉
'''
import datetime
import socket
import sys


DEFAULT_PORT=1234#默认端口

def timeServer(port):
    host=''#本机地址
    s=None
    for res in socket.getaddrinfo(host, port,
                                  socket.AF_UNSPEC,socket.SOCK_STREAM
                                  ,0,socket.AI_PASSIVE):#在本机的所有地址监听
        af,socktype,proto,canonname,sa=res
        try:
            s=socket.socket(af,socktype,proto)
        except socket.error,msg:
            s=None
            continue
        try:
            s.bind(sa)
            s.listen(10)
        except socket.error,msg:
            s.close()
            s=None
            continue
        break
    if s is None:
        print '不能生成socket对象'
        return 1
    while True:
        c,addr=s.accept()
        print '得到连接来自',addr
        c.send(str(datetime.datetime.now()))
        c.close()

if __name__=='__main__':
    port=DEFAULT_PORT
    if len(sys.argv)>1:
        try:
            port=int(sys.argv[1])
            if port<0 or port>65536:
                port=DEFAULT_PORT
        except Exception,e:
            port=DEFAULT_PORT
    timeServer(port)
        
        
        
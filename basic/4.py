#-*- coding: utf-8 -*-
'''
Created on 2016年10月9日

@author: 武明辉
'''
import socket


s=socket.socket()
server=socket.gethostname()
port=1234
s.connect((server,port))
print s.recv(1024)
s.close()


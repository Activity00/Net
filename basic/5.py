#-*- coding: utf-8 -*-
'''
Created on 2016年10月9日

@author: 武明辉
'''
import socket
import sys
import urlparse


def httpget(url):
    up=urlparse.urlparse(url)
    host=up[1]
    page=up[2]
    s=socket.socket()
    port=80
    s.connect((host,port))
    cmd='get'+page+'\n'
    s.send(cmd)
    print s.recv(1024)
    s.close()


if __name__=='__main__':
    httpget('https://github.com/')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 00:33:36 2020

@author: eriohoti
"""


import socket,os

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("192.168.2.10",1567))
img = open("test.jpg",'wb')
while True:
    incimg = s.recv(1024)
    if not incimg:
        break
    img.write(incimg)
img.close()
print('Complete!')

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat


import time
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 9000))

for i in range(30):
    client.send(b'wusir')
    msg = client.recv(1024)
    print(msg)
    time.sleep(.2)

client.close()

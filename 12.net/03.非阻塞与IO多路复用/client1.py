#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client1.py
# @Author:Mysticat


import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 阻塞
client.connect(('127.0.0.1', 9000))

while True:
    content = input('>>>')
    if content.upper() == 'Q':
        break
    client.sendall(content.encode('utf-8'))

client.close()

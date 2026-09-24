#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server1.py
# @Author:Mysticat

import time
import socket

sk = socket.socket()
sk.bind(('127.0.0.1',9000))
sk.listen()

conn,_ = sk.accept()
time.sleep(0.1)
msg1 = conn.recv(1024)
print(msg1)
msg2 = conn.recv(1024)
print(msg2)
conn.close()
sk.close()
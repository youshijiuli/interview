#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat

import struct
import socket

sk = socket.socket()
sk.connect(('127.0.0.1',9000))

msg = b'hello'
print(len(msg)) # 5
byte_len = struct.pack('i',len(msg)) # b'\x05\x00\x00\x00'
print(byte_len)
sk.send(byte_len)   #  1829137
sk.send(msg)        #  1829139
msg = b'world'
byte_len = struct.pack('i',len(msg))
sk.send(byte_len)
sk.send(msg)

sk.close()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_v2.py
# @Author:Mysticat


import socket
import json
import struct

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('127.0.0.1', 9000))
server.listen(5)


def myrecv(conn: socket.socket):
    len_bytes = conn.recv(4)
    len_obj_bytes = struct.unpack('i', len_bytes)[0]
    obj_bytes = conn.recv(len_obj_bytes)
    obj = json.loads(obj_bytes)
    return obj


conn, _ = server.accept()

file_info = myrecv(conn)

with open(file_info['filename'], 'wb') as f:
    while file_info['filesize'] > 0:
        content = conn.recv(1024)
        file_info['filesize'] -= len(content)
        f.write(content)
conn.close()

server.close()

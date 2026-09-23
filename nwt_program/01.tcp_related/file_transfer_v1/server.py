#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat


import os
import json
import struct
import socket

dir_path = ''

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('127.0.0.1', 9000))
server.listen(5)

while True:
    conn, addr = server.accept()

    print(addr)

    while True:
        try:

            cmd = conn.recv(1024)

            if not cmd:
                break
            file_name = cmd.split()[1].decode('utf-8')
            size = os.path.getsize(
                "%s%s" % (dir_path, file_name)
            )

            header_dic = {
                'filename': file_name,
                'total_size': size
            }

            header_str = json.dumps(header_dic)
            obj = struct.pack('q', len(header_str))
            conn.send(obj)
            conn.send(header_str.encode('utf-8'))
            with open(dir_path + str(file_name), 'rb') as f:
                for line in f:
                    conn.send(line)

        except Exception as error:
            print(error)
            break

    conn.close()

server.close()

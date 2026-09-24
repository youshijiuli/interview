#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat


import json
import struct
import socket
from utils.encrupt import md5_salt_username


class TcpServer(object):
    def __init__(self):
        self.dic = None
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.sk.bind(('127.0.0.1', 9000))
        self.sk.listen(5)

        self.conn, _ = self.sk.accept()

    def run(self):
        byte_len = self.conn.recv(1024)
        size = struct.unpack('i', byte_len)[0]
        jsondic = self.conn.recv(size)
        self.dic = json.loads(jsondic)
        print("self.dic的内容是%s" % self.dic)

        if self.dic:
            if self.dic['user_info'][0] == 'xp' and md5_salt_username(self.dic['user_info'][0],
                                                                      self.dic['user_info'][
                                                                          1]) == 'ea810eef63134accfb80c5983b835523':
                print('login sucess成功')
                self.conn.send(b'1')
            else:
                self.conn.send(b'0')

            return self.dic

    def put(self):
        file_len = self.conn.recv(4)
        file_size = struct.unpack('i', file_len)[0]
        print("接到的文件大小长度%s" % file_size)
        start_size = 0
        with open(self.dic['filename'], mode='ab') as f:
            while start_size < file_size:
                f.write(self.conn.recv(1024))
                start_size += 1024

        self.conn.close()
        self.sk.close()


server = TcpServer()
dic = server.run()

print(dic)

# if dic['user_info'][0] == 'xp' and md5_salt_username()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat


import socket
from config import settings


class Server(object):
    def __init__(self):
        self.host = settings.HOST
        self.port = settings.PORT

    def run(self, handler):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        server.bind((self.host, self.port))
        server.listen(5)
        while True:
            print('等待客户端链接....')
            conn, addr = server.accept()
            print(f'来自客户端{addr}的链接')
            instance = handler(conn)
            while True:
                result = instance.execute()
                if not result:
                    break
            conn.close()

        server.close()

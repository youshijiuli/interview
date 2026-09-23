#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat


import os
import json
import struct
import socket

from socket import SOL_SOCKET, SO_REUSEADDR

sock = socket.socket()

sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 9000))
sock.listen(5)


class Server(object):
    msg = {
        200: "register error, user exists！",
        201: "register successful",
        202: "login successful",
        203: "login error, user or password error",
    }

    user_info_path = './userinfo.json'

    def __init__(self):
        self.request, addr = sock.accept()

    def read_file(self):
        if not os.path.isfile(self.user_info_path):
            open(self.user_info_path, 'wb').close()
        with open(self.user_info_path, 'r', encoding='utf-8') as f:
            data = f.read()
            if data:
                return json.loads(data)
            else:
                return {}

    def write_file(self, data):
        with open(self.user_info_path, 'w', encoding='utf-8') as f:
            return json.dump(data, f)

    def send_msg(self, data):
        """
        发送数据
        :param data:
        :return:
        """
        head_data = json.dumps(data).encode('utf-8')
        head_size = struct.pack('i', len(head_data))
        self.request.send(head_size)
        self.request.send(head_data)

    def recv_msg(self):
        """
        接受数据
        :return:
        """
        head_size = self.request.recv(4)
        st_data = struct.unpack('i', head_size)[0]
        head_data = st_data.request.recv(st_data).decode('utf-8')
        return json.loads(head_data)

    def q(self):
        """ sever端退出 """
        exit('server exit......')

    def login(self, data):
        user_info = self.read_file()
        if data['user'] == user_info.get(data['user'])['user'] and data['pwd'] == user_info.get(data['user'])['pwd']:
            data['status'] = 202
            data['content'] = self.msg[202]
            data['login_status'] = True
        else:
            data['status'] = 203
            data['content'] = self.msg[203]
            data['login_status'] = False
        self.send_msg(data)

    def register(self, data):
        user_info = self.read_file()
        if data['user'] in user_info:
            data['status'] = 200
            data['content'] = self.msg[200]
        else:
            user_info[data['user']] = {"user": data['user'], "pwd": data['pwd']}
            self.write_file(user_info)
            data['status'] = 201
            data['content'] = self.msg[201]
        self.send_msg(data)

    def handler(self):
        while True:
            data = self.recv_msg()
            if hasattr(self, data['action_type']):
                getattr(self, data['action_type'])(data)

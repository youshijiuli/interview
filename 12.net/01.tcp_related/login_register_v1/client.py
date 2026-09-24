#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat


import json
import socket
import hashlib


class Client(object):
    login_status = False

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket()
        self.sock.connect((self.ip, self.port))

    def md5(self, pwd: str):
        return hashlib.md5(pwd.encode('utf-8')).hexdigest()

    def register(self):
        while True:
            user = input('user:').strip()
            pwd = input('pwd:').strip()
            if not user or not pwd:
                continue
            new_pwd = self.md5(pwd)
            data = {"user": user, 'pwd': new_pwd, "action_type": "register"}
            self.sock.send(
                json.dumps(data).encode('utf-8')
            )
            msg_data = self.sock.recv(1024).decode('utf-8')
            msg_data = json.loads(msg_data)
            if msg_data['code'] == 201:
                # 用户已经存在
                print(msg_data['msg'])
            else:
                print(msg_data['msg'])
                break

    def login(self):
        """
        用户登录
        :return:
        """
        if self.login_status:
            print('已为你自动登录...')
            return
        while True:
            user = input('user:').strip()
            pwd = input('pwd:').strip()
            if not user or not pwd:
                continue
            md_pwd = self.md5(pwd)
            data = {"user": user, "pwd": md_pwd, "action_type": "login"}
            self.sock.send(json.dumps(data).encode('utf-8'))
            msg_data = self.sock.recv(1024).decode('utf-8')
            msg_data = json.loads(msg_data)
            if msg_data['code'] == 301:
                print(msg_data['msg'])
                self.login_status = False
            else:
                print(msg_data['msg'])
                self.login_status = True
                break

    def q(self):
        """退出程序"""
        exit('你选择退出')

    def logout(self):
        """退出登录状态"""
        if self.login_status:
            self.login_status = False
            print('当前用户已经退出')
        else:
            print('用户没有登录')

    def handler(self):
        """
        专门用于和客户端转发消息的方法
        :return:
        """
        tmp_dict = {
            "1": ['登录', self.login],
            "2": ['注册', self.register],
            "3": ['退出', self.q],
            "4": ['退出登录状态', self.logout]
        }

        while True:
            for k, v in tmp_dict.items():
                print(k, v[0])

            choice = input('根据序号进行选择:').strip()
            if not choice:
                continue
            if tmp_dict.get(choice):
                tmp_dict.get(choice)[-1]()
            else:
                print('不支持的功能！！')


if __name__ == '__main__':
    client = Client('127.0.0.1', 8888)
    client.handler()

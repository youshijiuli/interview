#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat


import os
import json
import socket

BASE_DIR = os.path.dirname(
    os.path.abspath(
        __file__
    )
)


class Server(object):
    file_path = os.path.join(BASE_DIR, 'user.txt')
    msg_code = {
        200: "register successful",
        201: "user exits",
        300: "login successful",
        301: "user or password error"
    }

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((self.ip, self.port))
        self.sock.listen(5)

        # 如果不存在用户文件就创建
        if not os.path.isfile(self.file_path):
            open(self.file_path, 'wb').close()

    def register(self, data):
        """
        传递用户名，密码数据来注册用户
        :param data:
        :return:
        """
        print('register...', data)
        f = open(self.file_path, 'r', encoding='utf-8')
        for line in f:
            # line: zhangkai | 202cb962ac59075b964b07152d234b70
            user, pwd = line.strip().split('|')
            if user == data[user]:
                # 已经注册过，直接登录
                data['code'] = 201
                data['msg'] = self.msg_code[201]
                break

        # 用户没有注册过
        f.close()
        # 写入到文件
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(f'{data["user"]}|{data["pwd"]}\n')

        data['code'] = 200
        data['msg'] = self.msg_code[200]

        self.sock.send(json.dumps(data).encode('utf-8'))

    def login(self, data):
        """
        输入用户名密码完成用户登录
        :param data:
        :return:
        """
        print('login', data)
        f = open(self.file_path, 'r', encoding='utf-8')
        for line in f:
            user, pwd = line.strip().split('|')
            if user == data['user'] and pwd == data['pwd']:
                data['code'] = 300
                data['msg'] = self.msg_code[300]
                break

        f.close()
        if data['code'] != 300:
            # 表示登录失败
            data['code'] = 301
            data['msg'] = self.msg_code[301]

        self.conn.send(json.dumps(data).encode('utf-8'))

    def handler(self):
        """
        专门用于跟客户端转发消息的方法
        :return:
        """
        while True:
            # 链接循环
            print('等待客户端链接...')
            self.conn, addr = self.sock.accept()

            while True:
                # 消息循环
                print('等待客户端发送信息')
                try:
                    msg = self.conn.recv(1024).decode('utf-8')
                    if msg:
                        js_data = json.loads(msg)
                        if hasattr(self, js_data['action_type']):
                            method = getattr(self, js_data['action_type'])
                            method(js_data)
                        else:
                            self.conn.send('不支持的方法'.encode('utf-8'))
                    else:
                        print('客户端退出')
                        break
                except ConnectionResetError as error:
                    print('当前客户端异常断开', error)
                    break

            self.conn.close()
            print('客户端断开链接')
            break

        self.sock.close()


if __name__ == '__main__':
    obj = Server('127.0.0.1', 9000)
    obj.handler()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat


import struct
import socket
import os, json

# TODO:构造base_dir

BASE_DIR = ''


class TcpClient:

    def run(self):
        sk = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        sk.connect(('127.0.0.1', 9000))
        file_name = '公众号.png'
        path = os.path.join(
            BASE_DIR, file_name
        )
        name = input('输入用户名:').strip()
        pwd = input('输入密码:').strip()
        dic = {'cmd': 'put', 'filename': file_name, "user_info": [name, pwd]}
        json_dic = json.dumps(dic)
        byte_info = bytes(json_dic, encoding='utf-8')
        byte_len = struct.pack('i', len(byte_info))
        sk.send(byte_len)
        sk.send(byte_info)

        msg = sk.recv(1024)
        print(msg.decode('utf-8'))

        file_size = os.path.getsize(path)
        print("文件大小%s" % file_size)
        file_len = struct.pack('i', file_size)
        sk.send(file_len)
        print(f'文件长度:{file_len}')
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(1024)
                sk.send(chunk)
                if not chunk:
                    break
        sk.close()


client = TcpClient()
client.run()

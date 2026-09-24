#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :ftp_server.py
# @Author:Mysticat


import os
import sys
import json
import struct
import socket

REMOTE_DIR = os.path.join(os.path.dirname(__file__), 'remote')  # current_dir/remote


def myrecv(conn):
    num_by = conn.recv(4)
    msg_len = struct.unpack('i', num_by)[0]
    json_dic = conn.recv(msg_len).decode('utf-8')
    opt_dic = json.loads(json_dic)
    return opt_dic


def mysend(conn, dic):
    dic_bytes = json.dumps(dic).encode('utf-8')
    bytes_len = len(dic_bytes)
    send_len = struct.pack('i', bytes_len)
    conn.send(send_len)
    conn.send(dic_bytes)


def upload(conn):
    filename = opt_dic['filename']
    filesize = opt_dic['filesize']
    filepath = os.path.join(REMOTE_DIR, filename)
    with open(filepath, 'wb') as f:
        while filesize > 0:
            content = conn.recv(1024)
            f.write(content)
            filesize -= len(content)
            # 要接受的字节数不一定是你实际接收到的数据长度


def download(conn):
    file_path = os.path.join(REMOTE_DIR, opt_dic['filename'])
    if os.path.isfile(file_path):  # 判断是否存在这个文件
        size = os.path.getsize(file_path)  # 返回文件大小
        dic = {'filesize': size}
        mysend(conn, dic)
        with open(file_path, 'rb') as f:
            while size > 0:
                content = f.read(4096)
                conn.send(content)
                size -= len(content)


if __name__ == '__main__':
    sk = socket.socket()
    sk.bind(('127.0.0.1', 9001))
    sk.listen()
    while True:
        conn, addr = sk.accept()
        while True:
            try:
                opt_dic = myrecv(conn)
                if hasattr(sys.modules[__name__], opt_dic['operate']):
                    getattr(sys.modules[__name__], opt_dic['operate'])(conn)
            except:
                break
        conn.close()

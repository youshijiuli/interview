#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :ftp_client.py
# @Author:Mysticat


import os
import json
import struct
import socket

LOCAL_DIR = os.path.join(os.path.dirname(__file__), 'local')


def mysend(sk, opt_dic):
    opt_bytes = json.dumps(opt_dic).encode('utf-8')
    num_bytes = struct.pack('i', len(opt_bytes))
    sk.send(num_bytes)
    sk.send(opt_bytes)


def myrecv(sk):
    bytes_len = sk.recv(4)  # 要接受的数据的长度
    msg_len = struct.unpack('i', bytes_len)[0]
    str_dic = sk.recv(msg_len).decode('utf-8')  # 接收文件的大小
    size_dic = json.loads(str_dic)
    return size_dic


def upload(sk):
    path = input('请输入要上传的文件路径 : ')  # 用户输入要上传的文件
    if os.path.isfile(path):  # 检测这个文件是否存在
        filename = os.path.basename(path)  # 获取文件名
        filesize = os.path.getsize(path)  # 获取文件大小
        opt_dic = {'filename': filename, 'filesize': filesize, 'operate': 'upload'}  # 把请求发过去
        mysend(sk, opt_dic)
        # filesize = 16926596596198
        with open(path, 'rb') as f:
            while filesize > 0:
                content = f.read(4096)
                sk.send(content)
                filesize -= 4096


def download(sk):
    # remote文件夹中的所有文件你都可以下载
    filename = input('请输入要下载的文件名 : ')  # 用户输入一个文件名
    opt_dic = {'filename': filename, 'operate': 'download'}
    mysend(sk, opt_dic)
    size_dic = myrecv(sk)
    filepath = os.path.join(LOCAL_DIR, filename)
    with open(filepath, 'wb') as f:
        while size_dic['filesize'] > 0:
            content = sk.recv(1024)
            f.write(content)
            size_dic['filesize'] -= len(content)


if __name__ == '__main__':
    sk = socket.socket()
    sk.connect(('127.0.0.1', 9001))
    while True:
        # 选择 要做的操作 是上传 还是下载
        opt_lst = [('上传', upload), ('下载', download), ('退出', exit)]
        for index, opt in enumerate(opt_lst, 1):
            print(index, opt)
        inp = int(input('>>>').strip())
        opt_lst[inp - 1][1](sk) # 每一个函数需要socket作为参数

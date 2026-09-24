#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat


import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9000))

while True:
    download_file = input('请输入要下载的文件名:').strip()
    if download_file == '123':
        break
    client.send(download_file.encode('utf-8'))

client.close()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client2.py
# @Author:Mysticat


import socket
import threading


def receive_message():
    while True:
        message = client.recv(1024)
        print(f"收到消息：{message.decode('utf-8')}")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# host = socket.gethostname()
host = '127.0.0.1'
port = 9000

client.connect((host, port))

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

while True:
    message = input('请输入消息：')
    client.send(message.encode('utf-8'))
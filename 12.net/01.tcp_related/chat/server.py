#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server1.py
# @Author:Mysticat


import socket
import threading


def handle_client(client: socket.socket, addr):
    """
    处理客户端的请求
    :param client:
    :param addr:
    :return:
    """
    while True:
        message = client.recv(1024)
        if not message:
            break
        print(f"收到来自 {addr} 的消息：{message.decode('utf-8')}")
        boardcast(message, client)


def boardcast(message: str, sender: socket.socket):
    """
    消息广播
    :param message:
    :param sender:
    :return:
    """

    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clients = []
# host = socket.gethostname()
# print(host)
# input('---')
host = '127.0.0.1'
port = 9000
server.bind((host, port))
server.listen(5)

print(f'聊天室服务器正在监听{host}:{port}')

while True:
    client, addr = server.accept()
    print(f'有新的客户端:{client}连接{addr}')
    print(f'来自{addr}的客户端')
    clients.append(client)

    # 创建一个新的线程处理客户端
    client_handler = threading.Thread(target=handle_client, args=(client, addr))
    client_handler.start()

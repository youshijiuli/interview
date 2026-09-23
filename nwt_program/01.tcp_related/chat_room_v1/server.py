#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat


import os
import socket

user = {}


def do_login(s: socket.socket, name, addr):
    if name in user:
        s.send('用户已经存在'.encode('utf-8'), addr)
        return
    s.send(b'ok', addr)

    # 通知其他人
    msg = f'{name}进入聊天室'
    for i in user:
        s.sendto(msg.encode('utf-8'), user[i])

    # 插入字典
    user[name] = addr


def do_chat(s: socket.socket, name, text):
    msg = f'{name}:{text}'
    for i in user:
        if i != name:
            s.sendto(msg.encode('utf-8'), user[i])


def do_quit(s: socket.socket, name):
    msg = f'{name}退出来聊天室'
    for i in user:
        if i != name:
            s.sendto(msg.encode('utf-8'), user[i])

    del user[name]


# 循环来自客户端的请求
def do_request(s: socket.socket):
    while True:
        data, addr = s.recvfrom(1024)
        tmp = data.decode('utf-8').split(' ')
        if tmp[0] == 'L':
            do_login(s, tmp[1], addr)
        elif tmp[0] == 'C':
            text = " ".join(tmp[2:])
            do_chat(s, tmp[1], text)

        elif tmp[1] == 'Q':
            if tmp[1] not in user:
                s.sendto(b'EXIT', addr)
                continue
            do_quit(s, tmp[1])


# 搭建UDP服务
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9000))
    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        while True:
            msg = input('管理员消息：').strip()
            msg = "C 管理员消息 " + msg
            s.sendto(msg.encode('utf-8'), ('127.0.0.1', 9000))

    else:
        do_request(s)


# 共两个进程：一个父进程，一个子进程
# 父进程：处理所有客户端的请求。
# 　　　　udp无连接，s.sendto(内容,对方地址接口)。s始终为服务端的套接字。
# 子进程：发送管理员消息。


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat


import os, sys
import socket

ADDR = ('127.0.0.1', 8888)


def send_msg(s: socket.socket, name):
    """
    客户端发送信息
    :param s:
    :param name:
    :return:
    """
    while True:
        try:
            text = input('请输入信息：').strip()
        except KeyboardInterrupt:
            text = 'quit'
        if text == 'quit':
            msg = 'Q' + name
            s.sendto(msg.encode('utf-8'), ADDR)
            sys.exit('退出聊天室')

        msg = "C %s %s" % (name, text)
        s.sendto(msg.encode('utf-8'), ADDR)


def recv_msg(s: socket.socket):
    while True:
        try:
            data, addr = s.recvfrom(1024)
        except KeyboardInterrupt:
            sys.exit()

        if data.decode('utf-8') == 'EXIT':
            sys.exit()

        print(data.decode('utf-8') + f'\n发言', end='')


def main():
    """
    客户端启动
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        name = input('请输入姓名：').strip()
        msg = 'L' + name
        s.sendto(msg.encode('utf-8'), ADDR)

        # 等待反馈
        daat, addr = s.recvfrom(1024)
        if daat.decode('utf-8') == 'OK':
            print('您已经进入聊天室')
            break


        else:
            pass

    # 创建新的进程
    pid = os.fork()

    if pid < 0:
        sys.exit('ERROR')
    elif pid == 0:
        send_msg(s, name)
    else:
        recv_msg(s)


if __name__ == '__main__':
    main()

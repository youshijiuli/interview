#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat

import socket

# 阻塞io模型
# 非阻塞io模型
# 事件驱动io
# io多路复用
# 异步io模型


# socket的非阻塞io模型 + io多路复用实现的
# 虽然非阻塞，提高了CPU的利用率，但是耗费CPU做了很多无用功

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9000))
server.listen(5)

conn_list = []
del_list = []

while True:
    try:
        # 阻塞
        conn, addr = server.accept()
        print(conn)
        conn_list.append(conn)

    except BlockingIOError:
        for c in conn_list:
            try:
                msg = c.recv(1024).decode('utf-8')
                if not msg:
                    del_list.append(c)
                    continue
                print('-->', [msg])
                c.send(msg.upper().encode('utf-8'))
            except BlockingIOError:
                pass
        for c in del_list:
            conn_list.remove(c)
        del_list.clear()

server.close()

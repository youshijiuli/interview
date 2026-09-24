#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat


import select
from socket import *

server = socket(AF_INET, SOCK_STREAM)
server.bind(('127.0.0.1', 9000))
server.listen(5)

server.setblocking(False)
read_list = []

while True:
    r_list, w_list, x_list = select.select(read_list, [], [])
    """
    帮你监管
    一旦有人来了 立刻给你返回对应的监管对象
    """
    # print(res)  # ([<socket.socket fd=3, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 8080)>], [], [])
    # print(server)
    # print(r_list)

    for i in r_list:
        """针对不同的对象做不同的处理"""
        if i is server:
            conn, addr = i.accept()
            # 也要添加到监管队列中
            read_list.append(conn)

        else:
            res = i.recv(1024)
            if len(res) == 0:
                i.close()
                read_list.remove(i)
                continue
            print(res)
            i.send(b'sdiucghajhck')

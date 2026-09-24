#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server2.py
# @Author:Mysticat

from socket import *

server = socket(AF_INET, SOCK_STREAM)
server.bind(('127.0.0.1', 9000))
server.listen(5)

server.setblocking(False)

# 将所有的网络阻塞编程非阻塞

r_list = []
del_list = []

while True:
    try:
        conn, addr = server.accept()
        r_list.append(conn)

    except BlockingIOError:
        # time.sleep(0.1)
        # print('列表的长度:',len(r_list))
        # print('做其他事')

        for conn in r_list:
            try:
                data = conn.recv(1024)
                if len(data) == 0:
                    conn.close()
                    del_list.append(conn)
                    continue
                conn.send(data.upper())

            except BlockingIOError:
                continue
            except ConnectionError:
                conn.close()
                del_list.append(conn)

        # 清除无用的链接
        for conn in del_list:
            r_list.remove(conn)
        del_list.clear()

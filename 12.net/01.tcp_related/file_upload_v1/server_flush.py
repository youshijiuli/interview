#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat


"""文件上传，服务器接受用户上传的文件"""

import socket

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(('127.0.0.1',9000))

server.listen(5)

conn,addr = server.accept()

data = conn.recv(1024)
total_size = int(data.decode('utf-8'))


print(total_size,'.........')


file_obj = open('xxx.png', 'wb')
recv_size=  0


while True:
    data = conn.recv(1024)
    file_obj.write(data)
    file_obj.flush()

    recv_size += len(data)

    if recv_size == total_size:
        print('文件上传完毕')
        break

conn.close()
server.close()



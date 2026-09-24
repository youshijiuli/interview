#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat


import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9000))
server.listen(5)
print('服务器启动，监听端口9000...')

conn, addr = server.accept()
print(f'客户端 {addr} 已连接')

try:
    while True:
        data = conn.recv(1024)
        if not data:  # 客户端主动关闭连接
            break
        message = data.decode('utf-8')
        print(f'收到消息: {message}')

        if message.lower() == 'exit':  # 自定义退出指令
            conn.send(b'Server shutting down...')
            break

        conn.send(data.upper())

except KeyboardInterrupt:
    print('\n服务器被用户中断')
finally:
    conn.close()
    server.close()
    print('服务器已关闭')

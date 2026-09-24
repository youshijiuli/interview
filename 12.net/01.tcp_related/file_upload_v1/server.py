#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat


import tqdm
import socket

server = socket.socket(
    socket.AF_INET,socket.SOCK_STREAM
)

server.bind((
    '127.0.0.1',8001
))

server.listen(5)


# recv_data = b''

while True:
    rece_data = b''

    print('等待客户端链接....')
    conn,addr = server.accept()
    # 第一次接收文件名
    file_name = conn.recv(1024).decode('utf-8')
    print(f'客户端{addr}链接成功，准备接收文件:{file_name}')

    while True:
        data = conn.recv(1024)
        if not data:
            break
        rece_data += data

    if data.decode('utf-8') == 'exit':
        conn.close()
        break

    with open(f'upload_{file_name}','wb') as f:
        f.write(rece_data)

    conn.send('文件接受成功！'.encode('utf-8'))

    conn.close()


server.close()

# /Users/mac/PycharmProjects/code_pynet/03.tcp_base/file_upload_v1/test.txt


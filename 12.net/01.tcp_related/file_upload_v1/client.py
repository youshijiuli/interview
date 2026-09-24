#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat


import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 8001))

file_path = input('请输入文件路径:').strip()

file_name = file_path.split('/')[-1]

client.send(file_name.encode('utf-8'))



with open(file_path, 'rb') as f:
    data = f.read()

# 方案1,直接发送
client.send(data)
client.shutdown(socket.SHUT_WR)

# 方案一的BUG
# 1.文件大就难办，使用方案二，分块推送
# client.send(data)  # 如果 data 过大，可能超出系统发送缓冲区

# 2. 发送文件内容
# with open(file_path, 'rb') as f:
#     while True:
#         chunk = f.read(1024)  # 分块读取
#         if not chunk:
#             break
#         client.send(chunk)

# 3. 主动关闭写操作（关键！让服务端知道文件传输结束）
client.shutdown(socket.SHUT_WR)
recv_msg = client.recv(1024)

if recv_msg.decode('utf-8') != '文件接受成功！':
    print(f"上传失败: {recv_msg.decode('utf-8')}")

print(recv_msg.decode('utf-8'))

client.close()

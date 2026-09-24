#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat


import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9000))
print("已连接到服务器，输入'exit'退出")

try:
    while True:
        message = input(">>-- ")

        # 退出条件
        if message.lower() == 'exit':
            client.send(message.encode('utf-8'))  # 可选：通知服务器
            break

        # 发送消息
        client.send(message.encode('utf-8'))

        # 接收响应
        data = client.recv(1024)
        if not data:
            print("服务器已关闭连接")
            break

        print(f"服务器回复: {data.decode('utf-8')}")

except KeyboardInterrupt:
    print("\n客户端被用户中断")
except Exception as e:
    print(f"发生错误: {e}")
finally:
    # 确保无论如何都会关闭连接
    client.close()
    print("客户端已关闭")
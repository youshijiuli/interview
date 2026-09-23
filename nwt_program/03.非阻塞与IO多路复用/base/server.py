#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat

import socket
import select


"""
epoll演练

"""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9000))
server.listen(5)

# 申请epoll对象
epoll = select.epoll()

# 对server的这个套接字文件，注册可读事件
# 官方文档：https://docs.python.org/zh-cn/3.9/library/select.html?highlight=epoll#epoll-objects
# 对 server 套接字注册 可读事件

epoll.register(server.fileno(), select.EPOLLIN)
print('启动监听')
connections = {}
contents = {}

while True:
    # 通过系统调用，监听可读fds
    events = epoll.poll(10)  # 设置超时时间10秒
    for fileno, event in events:  # 文件描述符 及 事件
        if fileno == server.fileno():
            # 新链接
            s, addr = server.fileno()
            print('new conection from addr: ', addr)
            epoll.register(s.fileno(), select.EPOLLIN)
            connections[s.fileno()] = s
        # 2. 有服务套接字准备好了，读取数据
        elif event == select.EPOLLIN:
            s = contents[fileno]
            content = s.recv(1024)
            print(content)
            if not content:
                epoll.unregister(fileno)
                s.close()
                connections.pop(fileno)
            else:
                # 处理接收到的数据，并返回消息，修改事件为写事件
                content = content.upper()
                epoll.modify(fileno, select.EPOLLOUT)
                contents[fileno] = content

        elif event == select.EPOLLOUT:
            # 若出现网络异常
            try:
                content = contents[fileno]
                s = connections[fileno]
                s.send(content)
                # 发送完数据，再次修改为： 关注读事件
                epoll.modify(fileno, select.EPOLLIN)
            except:
                epoll.unregister(fileno)
                s.close()
                connections.pop(fileno)
                contents.pop(fileno)

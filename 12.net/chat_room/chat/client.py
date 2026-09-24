#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat

import json
import socket
from setting import header_struct


# 老是说没项目没项目，那有自己有没有认真做过一个项目
# 这个聊天室项目就是自己做的，虽然功能比较简单，但是自己从头到尾做下来，收获还是很大的

# 7.6 完成FTP   数理QT项目

# header_struct 定义在 settings.py 里
# struct 模块是一个 python 标准库
# 可以将一部分变量（包括int, 字符串等）打包成类似于 C 语言里结构体一样的东西
# 且长度固定，因此使得头部包长度固定。。。

def recvall(sock: socket.socket, length):
    # 接收客户端发送的包，无论是只有长度的包（头部包）还是正式消息的包（正文）
    # 由于头部包本身长度固定，所以接收的时候传入固定长度的length即可
    # 而在收到头部包之后，根据头部包里的内容（指示了正文有多长）传入length以接收接下来的正文
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError('socket closed with {} bytes left'
                           ' in this block'.format(length))
        length -= len(block)
        blocks.append(block)

    return b''.join(blocks)


def get_block(sock: socket.socket):
    """
    block:包，可以是头部包也可以是正文
    :param sock:
    :return:
    """
    data = recvall(sock, header_struct.size)
    # # unpack返回tuple，所以要加索引
    block_length = header_struct.unpack(data)[0]
    return recvall(sock, block_length)


def put_block(sock: socket.socket, content: str, info: str):
    """
    发送包，先发头部包，再发送正文
    :param sock:
    :param content:
    :param info:
    :return:
    """
    if len(info) <= 99:
        info += " " * (99 - len(info))
    content = info + content
    block_length = len(content)
    sock.send(header_struct.pack(block_length))
    sock.send(content.encode('utf-8'))


class Menu:
    def __init__(self):
        self.logged = False
        self.choices = {
            "1": self.login,
            "2": self.register,
            "3": self.query,
            "4": self.chat_with_all,
            "5": self.chat_with_one
        }  # 每个选项都对应了一个函数

    def display_menu(self):
        """
        1,2,3三个操作均在输入数字后显示结果，并再次出现这个菜单
        4,5两个操作在输入某一字符才退出，不然就一直和别人聊天。。
        :return:
        """
        print('''
               ----菜单

               --------1. 登录
               --------2. 注册
               --------3. 查询在线用户
               --------4. 群聊
               --------5. 与单一用户聊天
               ''')

    def login(self):
        """
        用户登录，如果已经登录就不允许再次登录
        :return:
        """
        if self.logged:
            return
        username = input('请输入用户名：')
        password = input('请输入密码：')

        login_info = username + " " + password
        # 正文包里的信息，指示服务器接下来要干啥。。当然服务器返回的包里也会有服务器定义的信息。。
        req_dict = {
            "command": 0,
            "from": username,
            "to": "server"
        }
        req_info = json.dumps(req_dict)

        # 发送包
        put_block(sock, login_info, req_info)

        # 接受包
        resp = get_block(sock).decode('utf-8')

        info = json.loads(resp[:99].rstrip(" "))

        cmd = info["command"]
        source = info["from"]
        to = info["to"]

        content = resp[99:]

        if content == 'success':
            print('登录成功！')
            self.logged = True
            return True
        print('登录失败')
        return False

    def query(self):
        pass

    def register(self):
        pass

    def chat_with_all(self):
        pass

    def chat_with_one(self):
        pass

    def run(self):
        while True:
            self.display_menu()
            choice = input("输入选项: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("无效选项，请重新输入: ")


if __name__ == '__main__':
    sock = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )
    sock.connect(('127.0.0.1', 9000))
    menu = Menu()
    menu.run()

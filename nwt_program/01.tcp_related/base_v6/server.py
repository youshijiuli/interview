#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat


# tcp协议的聊天
# 1.能和一个人聊之后再和另一个人聊
# 2.给每个人加颜色


import json
from socket import *

server = socket()
server.bind(('127.0.0.1', 9000))
server.listen()
color_dic = {
    '12345': {'color': '\033[32m', 'name': 'alex'},
    '12346': {'color': '\033[31m', 'name': 'wusir'},
    '12347': {'color': '\033[33m', 'name': 'yuan'},
}


def chat(conn):
    while True:
        msg = conn.recv(1024).decode('utf-8')
        dic_msg = json.loads(msg)
        uid = dic_msg['id']
        if dic_msg['msg'] == 'Q':
            print('%s已经下线' % color_dic[uid]['name'])
            break
        print('%s%s : %s\033[0m' % (color_dic[uid]['color'], color_dic[uid]['name'], dic_msg['msg']))
        inp = input('>>>')
        conn.send(inp.encode('utf-8'))
        if inp.upper() == 'Q':
            print('您已经断开和%s的聊天' % color_dic[uid]['name'])
            break


while True:
    conn, _ = server.accept()
    chat(conn)
    conn.close()
server.close()

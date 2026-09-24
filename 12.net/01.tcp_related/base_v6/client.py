#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat


import json
from socket import *

client = socket(AF_INET, SOCK_STREAM)

id = '123456'

client.connect(('127.0.0.1', 9000))

while True:
    msg = input('>>>').strip()
    dic = {'msg': msg, 'id': id}
    str_dic = json.dumps(dic)
    client.send(str_dic.encode('utf-8'))
    if msg.upper() == 'Q':
        print('您已经断开和server的聊天')
        break
    recv_msg = client.recv(1024).decode('utf-8')
    if recv_msg.upper() == 'Q':
        break
    print(recv_msg)
client.close()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import json

sk = socket.socket()

id = '12346'
sk.connect(('127.0.0.1',9000))
while True:
    inp = input('>>>')
    dic = {'msg':inp,'id':id}
    str_dic = json.dumps(dic)
    sk.send(str_dic.encode('utf-8'))
    if inp.upper()=='Q':
        print('您已经断开和server的聊天')
        break
    msg = sk.recv(1024).decode('utf-8')
    if msg.upper() == 'Q':
        break
    print(msg)
sk.close()






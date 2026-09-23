#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server2.py
# @Author:Mysticat


import json
import hashlib

with open('userinfo.json', 'r', encoding='utf-8') as f:
    # users = f.read()
    dic = json.load(f)

# print(users,type(users)) # <class 'str'>  json格式字符串
# 底层=
print(dic, type(dic))  # <class 'list'>
input('---')

from socket import *


def get_md5(username: str, password: str):
    md5_obj = hashlib.md5(username.encode('utf-8'))
    md5_obj.update(password.encode('utf-8'))
    return md5_obj.hexdigest()


server = socket(AF_INET, SOCK_STREAM)
server.bind(('127.0.0.1', 9000))
server.listen(5)

conn, _ = server.accept()
str_dic = conn.recv(1024).decode('utf-8')
obj_dic = json.loads(str_dic)

with open('userinfo.json', 'r', encoding='utf-8') as f:
    # users = f.read()
    users = json.load(f)
res_dic = {}

for user in users:
    if user['username'] == obj_dic['username'] and \
            user['password'] == get_md5(obj_dic['username'], obj_dic['password']):
        res_dic = {'opt': 'login', 'result': True}
        break
    else:

        res_dic = {'opt': 'login', 'result': False}

send_dic = json.dumps(res_dic)
conn.send(send_dic.encode('utf-8'))
conn.close()
server.close()

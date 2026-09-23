#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client2.py
# @Author:Mysticat


import json
from socket import *


username = input('请输入用户名:').strip()
password = input('请输入密码:').strip()
dic = {'username':username,'password':password}


str_dic = json.dumps(dic)
client = socket(AF_INET,SOCK_STREAM)
client.connect(('127.0.0.1',9000))

client.send(
    str_dic.encode('utf-8')
)

ret = client.recv(1024).decode('utf-8')
ret_dic = json.loads(ret)
if ret_dic['result']:
    print('登陆成功')
client.close()



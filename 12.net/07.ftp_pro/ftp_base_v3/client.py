#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat


import os
import json
import socket
import struct


client = socket.socket(
    socket.AF_INET,socket.SOCK_STREAM
)

def my_send(dic,encoding='utf-8'):
    str_dic = json.dumps(dic)
    bdic = str_dic.encode(encoding)
    len_dic = len(bdic)
    msg_len = struct.pack('i',len_dic)
    client.send(msg_len)
    client.send(bdic)


# 登录
username = input('请输入用户名:').strip()
password = input('请输入密码:').strip()
dic = {'operate': 'login', 'username': username, 'password': password}
my_send(dic)


msg_len = client.recv(4)
msg_len = struct.unpack('i',msg_len)[0]
str_dic = client.recv(msg_len).decode('utf-8')
dic = json.loads(str_dic)


if dic['operate'] == 'login' and dic['result']:
    print('login successfully!!!')


while True:
    file_path = input('请输入上传文件路径:').strip()
    if not os.path.isfile(file_path):
        print('文件不存在')
        continue # 下面的逻辑不会执行，直接循环再来一次
    filename = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)

    dic = {
        'operate':'uploda','filename':filename,'filesize':filesize
    }
    my_send(dic)

    with open(file_path,'rb')as f:
        while filesize>0:
            content = f.read(1024)
            client.send(content)
            filesize -= len(content)


client.close()




#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_v3.py
# @Author:Mysticat

import os
import json
import struct
import socket

def mysend(obj):
    obj_bytes = json.dumps(obj).encode('utf-8')
    blen_obj_bytes = struct.pack('i',len(obj_bytes))
    sk.send(blen_obj_bytes)
    sk.send(obj_bytes)

def myrecv():
    blen_obj_bytes=sk.recv(4)
    len_obj_bytes=struct.unpack('i',blen_obj_bytes)[0]
    obj_bytes=sk.recv(len_obj_bytes)
    obj=json.loads(obj_bytes.decode('utf-8'))
    return obj

sk = socket.socket()
sk.connect(('127.0.0.1',9017))

file_list=myrecv()

for index,item in enumerate(file_list,1):
    print(index,item)
download_num=int(input('请输入要下载的文件序号>>>').strip())

mysend(download_num)
fileinfo_dic=myrecv()

with open(fileinfo_dic['filename'],'wb') as f:
    while fileinfo_dic['filesize'] > 0:
        content = sk.recv(1024)
        fileinfo_dic['filesize'] -= len(content)
        f.write(content)

print('文件下载完毕！')
sk.close()
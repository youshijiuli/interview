#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_v3.py
# @Author:Mysticat


import json
import struct
import socket
import os

def mysend(obj):
    obj_bytes = json.dumps(obj).encode('utf-8')
    blen_obj_bytes = struct.pack('i',len(obj_bytes))
    conn.send(blen_obj_bytes)
    conn.send(obj_bytes)

def myrecv():
    blen_obj_bytes=conn.recv(4)
    len_obj_bytes=struct.unpack('i',blen_obj_bytes)[0]
    obj_bytes=conn.recv(len_obj_bytes)
    obj=json.loads(obj_bytes.decode('utf-8'))
    return obj

sk = socket.socket()
sk.bind(('127.0.0.1',9017))
sk.listen()
conn,_ =sk.accept()

dirpath=r'D:\软件'
file_list=os.listdir(dirpath)
for i in range(len(file_list)):
    file_list[int(i)]=os.path.join(dirpath,file_list[i])

mysend(file_list)
download_num=myrecv()

filepath = file_list[download_num-1]
filename = os.path.basename(filepath)
filesize = os.path.getsize(filepath)
fileinfo_dic = {'filename':filename,'filesize':filesize}

mysend(fileinfo_dic)

with open( filepath, mode = 'rb') as f:
    while filesize>0:
        content = f.read(1024)
        filesize -= len(content)
        conn.send(content)

print('文件传输完毕！')
conn.close()
sk.close()
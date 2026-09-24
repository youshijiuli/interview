#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_v2.py
# @Author:Mysticat


import os

import json
import socket
import struct

client = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)
client.connect(('127.0.0.1', 9000))


def mysend(obj):
    """
    先发送文件长度，再发送文件信息字典的字节数据
    :param obj:
    :return:
    """
    obj_bytes = json.dumps(obj).encode('utf-8')
    blen_obj_bytes = struct.pack('i', len(obj_bytes))
    client.send(blen_obj_bytes)
    client.send(obj_bytes)


path = './1.mp4'
filename = os.path.basename(path)
filesize = os.path.getsize(path)

file_info = {
    'filename': filename,
    'filesize': filesize
}

mysend(file_info)

with open(path, 'rb') as f:
    with filesize > 0:
        content = f.read(1024)
        filesize -= len(content)
        client.send(content)

print('文件上传完毕')
client.close()

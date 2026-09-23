#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat


import socket
import json
import struct

dir_download = './download/'

client = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)

client.connect(('127.0.0.1', 9000))

while True:
    cmd = input(">>>:").strip()
    if not cmd:
        continue
    fileanme = cmd.split()[1]
    client.send(cmd.encode('utf-8'))
    dic_size = struct.unpack("q", client.recv(8))[0]
    header_bytes = b''
    size = 0
    while size < dic_size:
        data = client.recv(1024)
        header_bytes += data
        size += len(data)

    header_dic = json.loads(header_bytes.decode('utf-8'))
    print(header_dic)

    total_size = header_dic['total_size']
    res_size = 0

    with open("%s%s" % (dir_download, fileanme), 'wb') as f:
        while True:
            data = client.recv(1024)
            res_size += len(data)
            f.write(data)
            # TODO:考虑一个进度条的功能
            print("=", res_size / total_size)

client.close()

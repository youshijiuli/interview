#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :index.py
# @Author:Mysticat


import socket
import struct
import os
import json

dir_share = "C:\\Users\\ASUS\\Desktop\\client\\share\\"
dir_download = "C:\\Users\\ASUS\\Desktop\\client\\download\\"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 8081))


def cmd_res(client):
    header_bytes_length = struct.unpack("i", client.recv(4))[0]
    header_bytes_size = 0
    header_bytes = b""
    while header_bytes_length > header_bytes_size:
        data = client.recv(1024)
        header_bytes += data
        header_bytes_size += len(data)
    header_dic = json.loads(header_bytes)
    print(header_dic)
    total_size = header_dic["total size"]
    res = b""
    res_size = 0
    while res_size < total_size:
        data = client.recv(1024)
        res += data
        res_size += len(data)
    print(res.decode("gbk"))


def get_res(cmd, filename, client):
    header_bytes_length = struct.unpack("i", client.recv(4))[0]
    header_bytes = b""
    header_bytes_size = 0
    while header_bytes_size < header_bytes_length:
        data = client.recv(1024)
        header_bytes += data
        header_bytes_size += len(data)
    header_dic = json.loads(header_bytes)
    print(header_dic)
    total_size = header_dic["total_size"]
    file_size = 0
    with open("%s%s" % (dir_download, filename), "wb") as f:
        while file_size < total_size:
            data = client.recv(1024)
            file_size += len(data)
            f.write(data)
            print("  ", str(float(file_size / total_size) * 100), "%")
    print(filename, "  ")


def put_res(cmd, client):
    filename = cmd.split()[1]
    total_size = os.path.getsize("%s%s" % (dir_share, filename))
    header_dic = {
        "type": " ???  ",
        "filename": filename,
        "total_size": total_size
    }
    header_bytes = json.dumps(header_dic)
    header_bytes_size = struct.pack("i", len(header_bytes))
    client.send(header_bytes_size)
    client.send(header_bytes.encode("utf-8"))
    with open("%s%s" % (dir_share, filename), "rb") as f:
        for line in f:
            client.send(line)
    print(filename)


def run():
    print("")
    print("")
    print("")
    while True:  #
        cmd = input(">>: ").strip()
        if not cmd:
            continue
        client.send(cmd.encode("utf-8"))
        lists = cmd.split()
        if lists[0] == "cmd":
            cmd_res(client)
        elif lists[0] == "get":
            filename = lists[3]
            get_res(cmd, filename, client)
        elif lists[0] == "put":
            put_res(cmd, client)
        else:
            print("")
            print("")
            print("")
            print("")
            continue
    client.close()


if __name__ == '__main__':
    run()

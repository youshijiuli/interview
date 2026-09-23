#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :index.py
# @Author:Mysticat


# coding=gbk
import socket
import subprocess
import struct
import json
import os

dir_share = "C:\\Users\\ASUS\\Desktop\\server\\share\\"
dir_download = "C:\\Users\\ASUS\\Desktop\\server\\download\\"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 8081))

server.listen(5)


def cmd_res(cmd, conn):
    conmand = cmd[4:]
    obj = subprocess.Popen(conmand.decode("gbk"), shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    stdout = obj.stdout.read()
    stderr = obj.stderr.read()
    header_dic = {
        "type": "   ?????   ",
        "total size": len(stderr) + len(stdout)
    }
    header_bytes = json.dumps(header_dic)
    header_bytes_length = struct.pack("i", len(header_bytes))
    conn.send(header_bytes_length)
    conn.send(header_bytes.encode("utf-8"))
    conn.send(stdout)
    conn.send(stderr)


def get_res(cmd, conn):
    filename = cmd.split()[1].decode("utf-8")
    total_size = os.path.getsize("%s%s" % (dir_share, filename))
    header_dic = {
        "type": "   ????  ",
        "filename": filename,
        "total_size": total_size
    }
    header_bytes = json.dumps(header_dic)
    header_bytes_length = struct.pack("i", len(header_bytes))
    conn.send(header_bytes_length)
    conn.send(header_bytes.encode("utf-8"))
    with open("%s%s" % (dir_share, filename), "rb") as f:
        for line in f:
            conn.send(line)


def put_res(cmd, filename, conn):
    header_bytes_length = struct.unpack("i", conn.recv(4))[0]
    header_bytes = b""
    header_bytes_size = 0
    while header_bytes_size < header_bytes_length:
        data = conn.recv(1024)
        header_bytes += data
        header_bytes_size += len(data)
    header_dic = json.loads(header_bytes)
    print(header_dic)
    total_size = header_dic["total_size"]
    res_size = 0
    with open("%s%s" % (dir_download, filename), "wb") as f:
        while res_size < total_size:
            data = conn.recv(1024)
            res_size += len(data)
            f.write(data)
    print(filename)


def run():
    # 链接循环
    while True:
        conn, addr = server.accept()
        print(addr)
        # 通信循环
        while True:
            try:
                cmd = conn.recv(8096)
                if not cmd:
                    break
                lists = cmd.split()
                if lists[0] == b"cmd":
                    cmd_res(cmd, conn)
                elif lists[0] == b"get":
                    get_res(cmd, conn)
                elif lists[0] == b"put":
                    filename = lists[3].decode("utf-8")
                    put_res(cmd, filename, conn)
            except ConnectionResetError:
                break
        conn.close()
        break
    server.close()


if __name__ == '__main__':
    run()

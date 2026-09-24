#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :file_transfer.py
# @Author:Mysticat

import os
import socket
import argparse


# 传输文件的测试代码。。。
# 很久之前写的，虽然能运行但跟不符合现在的代码结构，这一部分最后做吧。。。

def recvall(sock: socket.socket):
    data = b''
    while True:
        more = sock.recv(1024)
        data += more
        if len(more) < 1024:
            break
        return data


def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    path = './test.txt'
    file_name = os.path.basename(path)
    with open(file_name, 'rb') as f:
        content = f.read()
        sock.sendall(content)
        print('finishing reading the file')

    print('Successfully send the file')
    sock.shutdown(socket.SHUT_WR)
    print('connection closed')


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    sock.bind((interface, port))
    sock.listen(1)

    print(f"listing as {sock.getsockname()}")

    path = './recv.txt'

    while True:
        conn, addr = sock.accept()
        print(f"Got connecting from {addr}")
        print('receiving data...')

        data = recvall(conn)

        with open(path, 'wb') as f:
            print('file opened')
            print(f'data={data}')
            f.write(data)
            print('Srver:Done transfer')

        conn.close()


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description="transfer file")
    parser.add_argument('role', choices=choices)
    parser.add_argument('host')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060)
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)

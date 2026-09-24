#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat

import os
import time
import socket
from threading import Thread

# 全局变量
HOST = '0.0.0.0'
PORT = 8080
ADDR = (HOST, PORT)
FTP = "/home/tarena/FTP/"  # 文件库位置

# 非常简单的功能
# 1.获取文件列表
# 2.下载文件
# 3.上传文件


class FtpServer(Thread):

    def __init__(self, connfd):
        self.connfd = connfd
        super().__init__()

    def do_list(self):
        """
        获取文件列表
        :return:
        """
        fiels = os.listdir(FTP)
        if not fiels:
            self.connfd.send('文件目录为空'.encode('utf-8'))
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)

        # 开始传输数据
        fiels_ = ''
        for file in fiels:
            if file[0] != '.' and os.path.isfile(FTP + file):
                fiels_ += file + '\n'
            else:
                continue
        self.connfd.send(fiels_.encode('utf-8'))

    def do_get(self, filename):
        """
        客户端下载文件
        :param filename:
        :return:
        """
        file_path = FTP + filename
        exists = os.path.exists(file_path)
        if not exists:
            self.connfd.send('文件不存在'.encode('utf-8'))
            return

        fd = open(file_path, 'rb')
        self.connfd.send(b'OK')
        while True:
            data = fd.read(1024)
            if not data:
                time.sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)
        fd.close()

    def do_put(self,filename):
        """
        客户端上传文件
        :param filename:
        :return:
        """
        file_path = FTP + filename
        exists = os.path.exists(file_path)
        if exists:
            self.connfd.send('文件已经存在'.encode('utf-8'))
            return
        self.connfd.send(b'OK')
        f = open(file_path,'wb')
        while True:
            data = self.connfd.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()


    # v2
    # def do_put(self, filename):
    #     try:
    #         fd = open(FTP+filename, 'wb')
    #         #接受文件
    #         while True:
    #             data = self.connfd.recv(1024)
    #             if data == b'##':
    #                 break
    #             else:
    #                 fd.write(data)
    #         fd.close()
    #         raise Exception
    #     except:
    #         print("上传失败！")
    #         # data = '上传失败！'.encode()
    #         # self.connfd.send(data)　　#服务端上传失败，发送错误信息。

    def run(self):
        """
        循环接受客户端请求
        :return:
        """

        while True:
            data = self.connfd.recv(1024).decode('utf-8')  # 接受客户端的各种请求
            if not data or data == 'Q':
                return
            elif data == "L":
                self.do_list()
            elif data[0] == 'G':  # G filename
                filename = data.split(' ')[-1]
                self.do_get(filename)
            elif data[0] == 'P':  # P filename
                filename = data.split(' ')[-1]
                self.do_put(filename)


def main():
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    print("Listen the port %d..." % PORT)

    while True:
        try:
            connfd, addr = sockfd.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            print("服务器程序退出")
            return
        except Exception as e:
            print(e)
            continue

            # 创建新的线程处理客户端
        client = FtpServer(connfd)
        # client.setDaemon(True)
        client.daemon = True
        client.start()  # 运行run方法


if __name__ == '__main__':
    main()

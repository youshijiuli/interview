#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :client_flush.py
# @Author:Mysticat


import sys
import time
import socket

HOST = '0.0.0.0'
PORT = 8080
ADDR = (HOST, PORT)


class FtpClient:
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        """
        获取文件列表
        :return:
        """
        self.sockfd.send(b'L')
        data = self.sockfd.recv(1024).decode('utf-8')
        if data == 'OK':
            # 一次接受文件列表字符串
            data = self.sockfd.recv(1024)
            print(data.decode('utf-8'))
        else:
            print(data)

    def do_get(self, filename):
        """
        下载文件
        :param filename:
        :return:
        """
        self.sockfd.send(('G ' + filename).encode('utf-8'))
        data = self.sockfd.recv(1024).decode('utf-8')
        if data == 'OK':
            fd = open(filename, 'wb')
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)

    def do_put(self, filename):
        """
        上传文件
        :param filename:
        :return:
        """
        try:
            f = open(filename, 'rb')
        except Exception:
            print('文件不存在')
            return
        filename = filename.split('/')[-1]
        self.sockfd.send(('P ' + filename).encode('utf-8'))
        data = self.sockfd.recv(1024).decode('utf-8')

        if data == 'OK':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)

            f.close()
        else:
            print(data)

    # def do_put(self, rout, filename):
    #     try:
    #         fd = open(rout, 'rb')
    #     except Exception:
    #         print("文件不存在！")
    #         return
    #     else:
    #         self.sockfd.send(('P '+filename).encode())
    #         time.sleep(0.1)
    #     #文件发送
    #     while True:
    #         data = fd.read(1024)
    #         if not data:
    #             time.sleep(0.1)
    #             self.sockfd.send(b'##')
    #             break
    #         self.sockfd.send(data)
    #     # print(self.sockfd.recv(1024).decode())   #接受服务端的报错信息

    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit('感谢使用！！')


def main():
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print(e)
        return

    ftp = FtpClient(sockfd)

    while True:
        print("\n=========命令选项===========")
        print("*******    list      *******")
        print("*******    get file  *******")
        print("*******    put file  *******")
        print("*******    quit      *******")
        print("=============================")

        cmd = input("输入命令：").strip()

        if cmd == 'list':
            ftp.do_list()

        elif cmd[:3] == 'get':
            filename = cmd.strip(' ')[-1]
            ftp.do_get(filename)

        elif cmd[:3] == 'put':
            filename = cmd.strip(' ')[-1]
            ftp.do_put("/home/tarena/Secondclass/concurrent/day04/" + filename)
        elif cmd == 'quit':
            ftp.do_quit()

        else:
            print('请输入正确的命令！！！')
            continue


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_flush.py
# @Author:Mysticat

import os
import json
import struct
import socketserver

userinfo = './userinfo.txt'
server_dir = './server_dir'


def login(dic):
    flag = False
    with open(userinfo, 'r', encoding='utf-8') as f:
        for line in f:
            username, password = line.strip().split('|')
            print(username, password)
            if dic['username'] == username and dic['password'] == password:
                flag = True
                break

    return {'operate': 'login', 'result': flag}




def upload(dic):
    filepath = os.path.join(server_dir, dic['filename'])
    with open(filepath, 'wb') as f:
        while dic['filesize'] > 2048:
            content = dic['conn'].recv(2048)
            f.write(content)
            dic['filesize'] -= len(content)
        else:
            while dic['filesize']:
                content = dic['conn'].recv(dic['filesize'])
                f.write(content)
                dic['filesize'] -= len(content)



class MyServer(socketserver.BaseRequestHandler):
    def myrecv(self):
        """
        先接受登录，在接受上传/下载/创建文件夹
        :return:
        """
        msg_len = self.request.recv(4)
        msg_len = struct.unpack('i',msg_len)[0]
        str_dic = self.request.recv(msg_len).decode('utf-8')
        dic = json.loads(str_dic)
        return dic


    def mysend(self,dic):
        str_dic = json.dumps(dic)
        bdic = str_dic.encode('utf-8')
        len_dic = len(bdic)
        msg_len = struct.pack('i',len_dic)
        self.request.send(msg_len)
        self.request.send(bdic)


    def upload(self,dic):
        filepath = os.path.join(server_dir, dic['filename'])
        with open(filepath, 'wb') as f:
            while dic['filesize'] > 2048:
                content = self.request.recv(2048)
                f.write(content)
                dic['filesize'] -= len(content)
            else:
                while dic['filesize']:
                    content = self.request.recv(dic['filesize'])
                    f.write(content)
                    dic['filesize'] -= len(content)

    def handle(self) -> None:
        dic = self.myrecv()
        while True:
            if dic['operate'] == 'login':
                ret = login(dic)
                self.mysend(ret)
                if ret['result']:break

        while True:  # 用户登录成功之后执行
            if dic['operate'] == 'upload':
                dic['conn'] = self.request
                self.upload(dic)
            elif dic['operate'] == 'download':
                pass


server = socketserver.ThreadingTCPServer(('127.0.0.1',9000),MyServer)
server.serve_forever()
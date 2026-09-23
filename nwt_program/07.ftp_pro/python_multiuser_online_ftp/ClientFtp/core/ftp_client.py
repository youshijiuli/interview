#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 0021 0:13
# @Author  : lindian
# @FileName: ftp_client.py
# @Software: PyCharm

########################
# 客户端主程序
########################

import socket
import hashlib
import pickle
import struct
import os
import sys

from conf import settings

class FTPClient:
    """
    实现与服务端之间的交互
    功能:

    """
    def __init__(self, server_address, connect=True):
        """
        构造方法,创建实例对象自动执行
        :param server_address: IP和端口
        :param connect: 连接状态
        """
        self.server_address = server_address    # IP端口信息
        self.socket = socket.socket()   # 设置socket对象
        if connect:
            try:
                self.client_connect()   # 连接服务端
            except Exception:
                self.client_close()     # 关闭连接

    def client_connect(self):
        """
        连接服务端
        :return:
        """
        try:
            self.socket.connect(self.server_address)    # 建立连接通道
        except Exception as e:
            print("错误: %s" % e)
            exit("服务器未激活")

    def client_close(self):
        """
        关闭连接
        :return:
        """
        self.socket.close()

    def get_recv(self):
        """
        接收服务端发来的的数据
        :return:
        """
        return pickle.loads(self.socket.recv(settings.max_recv_bytes))

    def login(self):
        """
        用户登录, 超过三次则退出
        账户密码发送到server进行认证
        响应服务端信息, 成功返回1, 失败返回0
        :return: 如果账户密码正确,返回用户数据字典
        """
        retry_count = 0     # 重试次数初始值
        while retry_count < 3:
            username = input("请输入用户名>>").strip()
            if not username:
                continue
            password = input("请输入密码>>").strip()
            if not password and not password.isdigit():
                continue
            # 账户密码
            user_dic = {
                'username': username,
                'password': password,
            }
            # 发送账户密码到服务端进行认证,并接收数据(一发一收)
            data = pickle.dumps(user_dic)     # 序列化
            self.socket.send(data)  # 发送数据
            # 为了防止出现黏包问题，所以先解压包头，读取包头，再读数据
            obj = self.socket.recv(4)   # 接收数据(接收的数据是bytes类型)
            res = struct.unpack('i', obj)[0]    # 解包(读取二进制数据以元组形式返回) i表示int格式
            # 此处,如果返回代码1,则成功 0则失败
            if res:
                print("------------- 欢迎来到FTP客户端 --------------")
                user_info_dic = self.get_recv()
                recv_username = user_info_dic['username']
                return True
            else:
                print("帐号或密码不正确！")
        retry_count += 1

    def recv_file_header(self, header_size):
        """
        接收文件的header, filename, file_size, file_md5
        :param header_size:
        :return:
        """
        header_types = self.socket.recv(header_size)    # 接收数据
        header_dic = pickle.loads(header_types)     # 反序列化
        print(header_dic, type(header_dic))
        total_size = header_dic['file_size']
        filename = header_dic['filename']
        file_md5 = header_dic['file_md5']
        return (filename, total_size, file_md5)

    def progress_bar(self, num, get_size, file_size):
        """
        显示进度条
        :param num:
        :param get_size:
        :param file_size:
        :return:
        """
        float_rate = float(get_size) / float(file_size)
        rate_num = round(float_rate * 100, 2)
        if num == 1:  # 1表示下载
            sys.stdout.write('\033[31;1m\r完成下载权限：{0}%\033[0m'.format(rate_num))
        elif num == 2:  # 2表示上传
            sys.stdout.write('\033[31;1m\r完成上传内容：{0}%\033[0m'.format(rate_num))
        sys.stdout.flush()

    def appendfile_content(self, file_path, temp_file_size, file_size):
        """
        追加文件内容
        :param file_path:
        :param temp_file_size:
        :param file_size:
        :return:
        """
        with open(file_path, 'ab') as f:
            f.seek(temp_file_size)
            get_size = temp_file_size
            while get_size < file_size:
                res = self.socket.recv(settings.max_recv_bytes)
                f.write(res)
                get_size += len(res)
                self.progress_bar(1, get_size, file_size)  # 显示进度条 1表示下载


    def verification_filemd5(self, file_md5):
        """
        校验文件md5
        :param filemd5:
        :return:
        """
        # 判断下载下来的文件MD5值和server传过来的MD5值是否一致
        if self.getfile_md5() == file_md5:
            print('\033[31;1m 下载成功 \033[0m')
        else:
            print('\033[31;1m 抱歉下载失败，再次下载断点续传 \033[0m')

    def write_file(self, f, get_size, file_size):
        """
        下载文件，将内容写入文件中
        :param f:
        :param get_size:
        :param file_size:
        :return:
        """
        while get_size < file_size:
            res = self.socket.recv(settings.max_recv_bytes)
            f.write(res)
            get_size += len(res)
            self.progress_bar(1, get_size, file_size)  # 1表示下载

    def get(self, cmds):
        """
        从服务端下载文件
        :param cmd: 指令列表
        :return:
        """
        if len(cmds) > 1:
            filename = cmds[1]  # 获取文件名
            # 下载文件的存放路径
            self.file_path = os.path.join(settings.down_file_path, filename)
            # 如果文件存在,则支持断点续传
            if os.path.isfile(self.file_path):
                temp_file_size = os.path.getsize(self.file_path)    # 文件大小
                self.socket.send(struct.pack('i', temp_file_size))  # 发送打包好的数据给服务端
                header_size = struct.unpack('i', self.socket.recv(4))[0]    # 接收数据解包
                if header_size:
                    filename, file_size, file_md5 = self.recv_file_header(header_size)
                    if temp_file_size == file_size:
                        print("文件已经存在!")
                    else:
                        print("文件现在是断点续集.")
                        self.appendfile_content(self.file_path, temp_file_size)
                        self.verification_filemd5(file_md5)
                else:
                    print("以前下载文件，但现在服务器的文件不存在")
            # 如果文件不存在,直接下载
            else:
                self.socket.send(struct.pack('i', 0))
                obj = self.socket.recv(1024)
                header_size = struct.unpack('i', obj)[0]
                if header_size == 0:
                    print("文件不存在！")
                else:
                    filename, file_size, file_md5 = self.recv_file_header(header_size)
                    # 下载文件路径
                    download_filepath = os.path.join(settings.down_file_path, filename)
                    with open(download_filepath, 'wb') as f:
                        get_size = 0
                        self.write_file(f, get_size, file_size)
                    self.verification_filemd5(file_md5)
        else:
            print("没有输入文件名!")

    def readfile(self):
        """
        读取文件
        """
        with open(self.file_path, 'rb') as f:
            filedata = f.read()
        return filedata

    def getfile_md5(self):
        """
        对文件内容进行加密，也就是保持文件的一致性
        """
        md5 = hashlib.md5(self.readfile())
        print("md5是：\n", md5.hexdigest())
        return md5.hexdigest()

    def open_sendfile(self, file_size, recv_size=0):
        """
        打开要上传的文件（由于本程序上传文件的原理是先读取本地文件，再写到上传地址的文件）
        """
        with open(self.file_path, 'rb') as f:
            # send_bytes = b''
            # send_size = 0
            f.seek(recv_size)
            while True:
                data = f.read(1024)
                if data:
                    self.socket.send(data)
                    obj = self.socket.recv(4)
                    recv_size = struct.unpack('i', obj)[0]
                    self.progress_bar(2, recv_size, file_size)
                else:
                    break
        success_state = struct.unpack('i', self.socket.recv(4))[0]
        if success_state:
            print('\033[31;1m祝贺上传成功\033[0m')
        else:
            print('\033[31;1m抱歉上传目录失败\033[0m')

    def put_situation(self, file_size, condition=0):
        """
        上传的时候有两种情况，文件已经存在，文件不存在
        """
        quota_state = struct.unpack('i', self.socket.recv(4))[0]
        if quota_state:
            if condition:
                obj = self.socket.recv(4)
                recv_size = struct.unpack('i', obj)[0]
                self.open_sendfile(file_size, recv_size)
            else:
                self.open_sendfile(file_size)
        else:
            print('\033[31;1m抱歉超过用户配额\033[0m')

    def put(self, cmds):
        """
        往server端登录的用户目录下上传文件
        """
        if len(cmds) > 1:
            filename = cmds[1]
            self.file_path = os.path.join(settings.upload_file_path, filename)
            print(self.file_path)
            if os.path.isfile(self.file_path):  # 如果文件存在，支持断电续传
                self.socket.send(struct.pack('i', 1))
                file_size = os.path.getsize(self.file_path)
                header_dic = {
                    'filename': os.path.basename(filename),
                    'file_md5': self.getfile_md5(),
                    'file_size': file_size
                }
                header_bytes = pickle.dumps(header_dic)
                self.socket.send(struct.pack('i', len(header_bytes)))
                self.socket.send(header_bytes)
                state = struct.unpack('i', self.socket.recv(4))[0]
                if state:  # 已经存在
                    has_state = struct.unpack('i', self.socket.recv(4))[0]
                    if has_state:
                        self.put_situation(file_size, 1)
                    else:  # 存在的大小 和文件大小一致 不必再传
                        print("\033[31;1m文件已经存在！\033[0m")
                else:  # 第一次传
                    self.put_situation(file_size)
            else:  # 文件不存在
                print("\033[31;1m文件不存在！\033[0m")
                self.socket.send(struct.pack('i', 0))
        else:
            print("\033[31;1m用户没有输入文件名\033[0m")

    def ls(self, cmds):
        """
        查看当前工作目录，文件列表
        """
        print("\033[34;1m查看当前工作目录\033[0m")
        obj = self.socket.recv(4)
        dir_size = struct.unpack('i', obj)[0]
        recv_size = 0
        recv_bytes = b''
        while recv_size < dir_size:
            temp_bytes = self.socket.recv(settings.max_recv_bytes)
            recv_bytes += temp_bytes
            recv_size += len(temp_bytes)
        print(recv_bytes.decode('gbk'))

    def mkdir(self, cmds):
        '''增加目录
        1，server返回1 增加成功
        2，server返回2 增加失败'''
        print("\033[34;1m添加工作目录\033[0m")
        obj = self.socket.recv(4)
        res = struct.unpack('i', obj)[0]
        if res:
            print('\033[31;1m祝贺添加目录成功\033[0m')
        else:
            print('\033[31;1m对不起添加目录失败\033[0m')

    def cd(self, cmds):
        '''切换目录'''
        print("\033[34;1m交换机工作目录\033[0m")
        if len(cmds) > 1:
            obj = self.socket.recv(4)
            res = struct.unpack('i', obj)[0]
            if res:
                print('\033[31;1m祝贺转换目录成功\033[0m')
            else:
                print('\033[31;1m对不起开关目录失败\033[0m')
        else:
            print("\033[31;1m用户不输入文件名\033[0m")

    def remove(self, cmds):
        '''表示删除文件或空文件夹'''
        print("\033[34;1m删除工作目录\033[0m")
        obj = self.socket.recv(4)
        res = struct.unpack('i', obj)[0]
        if res:
            print('\033[31;1m祝贺成功\033[0m')
        else:
            print('\033[31;1m删除目录失败\033[0m')

    def execute(self):
        """
        开始执行
        :return:
        """
        if self.login():    # 进行用户登录认证
            while True:
                try:
                    self.help_info()
                    choice = input("请输入命令>>").strip()
                    if not choice:
                        continue
                    self.socket.send(choice.encode(settings.coding))   # 向服务端发送数据
                    cmds = choice.split()
                    if hasattr(self, cmds[0]):  # 判断是否存在对象cmds[0]属性
                        func = getattr(self, cmds[0])   # 获取类中的方法对象
                        func(cmds)  # 执行指定命令的方法
                        break
                    else:
                        print("没有这样的命令，请再试一次。")
                except Exception as e:
                    print("错误: %s" % e)
                    break

    def help_info(self):
        """
        帮助信息
        :return:
        """
        print('''\033[34;1m
    get + (文件名）    表示下载文件
    put + (文件名）    表示上传文件
    ls                 表示查询当前目录下的文件列表（只能访问自己的文件列表）
    mkdir + (文件名）  表示创建文件夹 
    cd + (文件名）     表示切换目录（只能在自己的文件列表中切换）
    remove + (文件名） 表示删除文件或空文件夹
        \033[0m''')

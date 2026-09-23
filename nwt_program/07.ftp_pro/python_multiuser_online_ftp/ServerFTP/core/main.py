#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 0021 20:04
# @Author  : lindian
# @FileName: main.py
# @Software: PyCharm

####################
# 服务端主程序
####################

from core.user_handle import UserHandle
from core.ftp_server import FTPServer
from conf import settings

class Manager:
    """
    主程序 包括启动server, 创建用户, 退出
    """
    def start_ftp(self):
        """
        启动ftp
        :return:
        """
        server = FTPServer(settings.ip_port)    # 实例化FTP类
        server.server_link()    # 服务器连接 等待客户端发送数据
        server.close()  # 关闭

    def create_user(self):
        """
        创建用户,执行创建用户的类
        :return:
        """
        username = input("请输入您的用户名>>").strip()
        if username:
            UserHandle(username).add_user()     # 执行类中创建用户的方法

    def logout(self):
        """
        退出程序
        :return:
        """
        print("已退出!")
        exit()

    def interactive(self):
        """
        用户交互
        :return:
        """
        msg = '''\033[32;1m
    1   启动ftp服务端
    2   创建用户
    3   退出
               \033[0m'''
        menu_dic = {
            "1": 'start_ftp',
            "2": 'create_user',
            "3": 'logout',
        }
        exit_flag = False
        while not exit_flag:
            print(msg)
            user_choice = input("请输入指令>>").strip()
            if user_choice in menu_dic:
                getattr(self, menu_dic[user_choice])()  # 获取类属性值,并执行方法
            else:
                print("没有这个选项!")

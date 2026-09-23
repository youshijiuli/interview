#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 0021 21:50
# @Author  : lindian
# @FileName: user_handle.py
# @Software: PyCharm

####################
# 创建用户
####################

import configparser
import hashlib
import os

from conf import settings

class UserHandle:
    """
    创建用户
    如果用户存在则返回, 不存在则注册成功
    """
    def __init__(self, username):
        self.username = username
        # 创建一个配置文件对象
        self.config = configparser.ConfigParser()
        # 读取配置文件
        self.config.read(settings.ACCOUNTS_FILE)

    @property
    def disk_quota(self):
        """
        生成每个用户的磁盘配额
        :return:
        """
        quota = input("请输入磁盘配额>>").strip()
        if quota.isdigit():
            return quota
        else:
            print("磁盘配额必须是整数!")

    @property
    def password(self):
        """
        生成用户的默认密码
        :return: 加密后的密码
        """
        while True:
            password_inp = input("请输入您的密码>>").strip()
            if password_inp is not None and password_inp.isdigit():
                md5_obj = hashlib.md5()     # 创建一个md5对象
                md5_obj.update(password_inp.encode())   # 密码进行md5加密
                md5_password = md5_obj.hexdigest()  # 获取十六进制密文
                return md5_password
            else:
                print("输入错误!")

    def add_user(self):
        """
        创建用户,存储到accounts.ini文件
        :return:
        """
        # 配置文件不存在username的section
        if not self.config.has_section(self.username):
            print("创建用户名是：%s" % self.username)
            # 添加新用户的section
            self.config.add_section(self.username)
            # 为section添加option(键值对)
            self.config.set(self.username, 'password', self.password)   # 通过property属性调用方法
            self.config.set(self.username, 'home_dir', 'home/' + self.username)
            self.config.set(self.username, 'quota', self.disk_quota)    # 通过property属性调用方法
            with open(settings.ACCOUNTS_FILE, 'w') as f:
                self.config.write(f)    # 写入配置文件
            # 创建用户的home文件夹
            os.mkdir(os.path.join(settings.BASE_DIR, 'home', self.username))
            print("成功创建用户数据.")
        else:
            print("用户名已经存在!")

    def judge_user(self):
        """
        判断用户是否存在
        :return: 用户section的option
        """
        if self.config.has_section(self.username):
            return self.config.items(self.username)

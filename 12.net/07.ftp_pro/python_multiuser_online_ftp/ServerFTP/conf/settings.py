#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 0021 19:54
# @Author  : lindian
# @FileName: settings.py
# @Software: PyCharm

###############
# 配置信息
###############

import os
import sys
import socket

# 绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 账户信息存储文件
ACCOUNTS_FILE = os.path.join(BASE_DIR, 'conf', 'accounts.ini')

address_family = socket.AF_INET
socket_type = socket.SOCK_STREAM

# 绑定的IP
BIND_HOST = '127.0.0.1'
# 绑定的端口
BIND_PORT = 9999
ip_port = (BIND_HOST, BIND_PORT)

# 编码格式
coding = 'utf8'

# 最大接收值
max_recv_bytes = 8192

# socket监听连接次数
listen_count = 5

#
allow_reuser_address = False

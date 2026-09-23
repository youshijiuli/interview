#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 0021 0:12
# @Author  : lindian
# @FileName: settings.py
# @Software: PyCharm

##################
# 配置信息
##################

import os
import sys
import socket

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 下载文件的储存路径
down_file_path = os.path.join(BASE_DIR, 'download')
# 上传文件的储存路径
upload_file_path = os.path.join(BASE_DIR, 'upload')

# 绑定的IP地址
BIND_HOST = '127.0.0.1'
# 绑定的端口
BIND_PORT = 9999
ip_port = (BIND_HOST, BIND_PORT)
address_family = socket.AF_INET     # 表示IPV4(默认)
socket_type = socket.SOCK_STREAM    # 流式socket for TCP（默认）

# 编码格式
coding = 'utf8'
# 最大的返回值
max_recv_bytes = 8192
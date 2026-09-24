#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 0021 0:04
# @Author  : lindian
# @FileName: run.py
# @Software: PyCharm

####################
# 客户端入口
####################

import os
import sys

BAES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BAES_DIR)

from core import ftp_client
from conf import settings

if __name__ == '__main__':
    run = ftp_client.FTPClient(settings.ip_port)
    run.execute()

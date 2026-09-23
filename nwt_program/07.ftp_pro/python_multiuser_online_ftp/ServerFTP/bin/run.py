#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 0021 19:49
# @Author  : lindian
# @FileName: run.py
# @Software: PyCharm

###################
# 服务端入口
###################

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import main

if __name__ == '__main__':
    a = main.Manager()
    a.interactive()

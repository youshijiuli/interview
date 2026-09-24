#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :settings.py
# @Author:Mysticat


import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# /xxx/.../server


HOST = "0.0.0.0"
PORT = 9997

USER_HOME_DIR = os.path.join(BASE_DIR, "home")

ACCOUNT_DIR = "%s/conf/account.ini" % BASE_DIR

MAX_SOCKET_LISTEN = 5
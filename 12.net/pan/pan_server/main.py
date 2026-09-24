#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Author:Mysticat

from src.handlers.pan import PandHandler
from src.server import Server
# from src.select_server import SelectServer

if __name__ == '__main__':
    server = Server()
    server.run(PandHandler)

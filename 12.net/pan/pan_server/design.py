#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :design.py
# @Author:Mysticat


class PanHandler(object):
    def execute(self):
        pass


class BaseServer(object):

    def run(self, handler_class):
        panhandler = handler_class()
        panhandler.execute()


class SelectServer(object):

    # 基于IO多路复用的socket服务端
    def run(self, handler_class):
        panhandler = handler_class()
        panhandler.execute()


if __name__ == '__main__':
    server = BaseServer()

    server.run()

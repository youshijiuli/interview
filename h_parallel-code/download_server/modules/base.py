#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :base.py
# @Author:Mysticat


# hash模块和 下载模块结构基本一致，这里抽象出来就可以
from download_server.const import CalcType


class BaseModel(object):

    def __init__(self):
        self.calType = CalcType.singleThread

    def set_cal_type(self, type_):
        self.calType = type_

    def _process(self, item):
        pass

    def _process_singlethread(self, list_):
        """ 单线程处理函数 """
        pass

    def _process_multithread(self, list_):
        """ 多线程处理函数 """
        pass

    def _process_multiprocess(self, list_):
        """ 多进程处理函数 """
        pass

    def process(self, list_):
        if self.calType == CalcType.singleThread:
            return self._process_singlethread(list_)
        elif self.calType == CalcType.MultiProcess:
            return self._process_multiprocess(list_)
        elif self.calType == CalcType.MultiThread:
            return self._process_multithread(list_)
        else:
            pass

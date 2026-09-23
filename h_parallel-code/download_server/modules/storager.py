#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :storager.py
# @Author:Mysticat


# 图片存储模块
from download_server.modules.base import BaseModel

from PIL import Image
from download_server.modules.executors import thread_pool_executor as tp
from download_server.modules.executors import process_pool_executor as pp


class Storage(BaseModel):
    """ 存储模块 """

    def _process(self, item):
        print('调用存储模块')
        content, path = item
        content = Image.fromarray(content.astype('uint8')).convert('RGB')
        content.save(path)

    def _process_singlethread(self, list_):
        """列表中每一个元素包含的是 (content, path)，内容和存储路径"""
        for item in list_:
            self._process(item)

    def _process_multithread(self, list_):
        """ 多线程 """
        task_list = []
        for item in list_:
            task = tp.submit(self._process, (item))
            task_list.append(task)

        for task in task_list:
            task.result()

    def _process_multiprocess(self, list_):
        """ 多进程 """
        task_list = []
        for item in list_:
            task = pp.submit(self._process, (item))
            task_list.append(task)

        for task in task_list:
            task.result()

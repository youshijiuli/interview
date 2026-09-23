#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :downloader.py
# @Author:Mysticat


# 下载模块
import requests
from PIL import ImageFile
import numpy as np

from download_server.modules.base import BaseModel
from download_server.modules.executors import thread_pool_executor as tp
from download_server.modules.executors import process_pool_executor as pp


class Downloader(BaseModel):
    """ 下载模块 """

    def __init__(self):
        super(Downloader, self).__init__()

    def _process(self, url):
        """ 处理图片的下载：任务 """
        print("下载链接为： {}.".format(url))
        response = requests.get(url)
        content = response.content
        # 为了方便后面的hash模块以及存储模块的处理，把图片二进制内容，转成 numpy数组
        parser = ImageFile.Parser()
        parser.feed(content)
        img = parser.close()
        img = np.array(img)
        return img

    def _process_singlethread(self, list_):
        """ 单线程 """
        response_list = []
        for url in list_:
            # 图片下载
            img = self._process(url)
            response_list.append(img)
        return response_list

    def _process_multithread(self, list_):
        """ 多线程 """
        response_list = []
        task_list = []
        for url in list_:
            # task 保存future对象
            task = tp.submit(self._process, (url))
            task_list.append(task)
        for task in task_list:
            img = task.result()
            response_list.append(img)

        return response_list

    def _process_multiprocess(self, list_):
        """ 多线程处理函数 """
        response_list = []
        task_list = []
        for url in list_:
            task = pp.submit(self._process, (url))
            task_list.append(task)

        for task in task_list:
            img = task.result()
            response_list.append(img)

        return response_list

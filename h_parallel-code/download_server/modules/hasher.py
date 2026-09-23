#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :hasher.py
# @Author:Mysticat


# 实现图片内容的hash，得到MD5的字符串
from download_server.modules.base import BaseModel
from scipy import signal
from PIL import Image, ImageFile
import hashlib
from download_server.modules.executors import thread_pool_executor as tp
from download_server.modules.executors import process_pool_executor as pp


class Hasher(BaseModel):

    def _process(self, item):
        """
        卷积
        :param item:
        :return:
        """
        cov = [[[0.1], [0.05], [0.1]]]
        img = signal.convolve(item, cov)

        img = Image.fromarray(img.astype('uint8')).convert('RGB')
        return hashlib.md5(str(img).encode('utf-8')).hexdigest()

    def _process_singlethread(self, list_):
        """ 单线程处理函数
            hash的计算
        """
        md5_list = []
        for img in list_:
            md5 = self._process(img)
            md5_list.append(md5)

        return md5_list

    def _process_multithread(self, list_):
        """ 多线程 """
        md5_list = []
        task_list = []
        for img in list_:
            task = tp.submit(self._process, (img))
            task_list.append(task)

        for task in task_list:
            md5 = task.result()
            md5_list.append(md5)
        return md5_list

    def _process_multiprocess(self, list_):
        """ 多进程处理函数 """
        md5_list = []
        task_list = []
        for img in list_:
            task = pp.submit(self._process, (img))
            task_list.append(task)

        for task in task_list:
            md5 = task.result()
            md5_list.append(md5)
        return md5_list

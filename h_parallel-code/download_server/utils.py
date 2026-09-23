#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :utils.py
# @Author:Mysticat


import os
import time


def get_url_list():
    """ 加载文件，并返回下载链接 """
    url_list = []
    file_path = './piclist/baidu.txt'
    with open(file_path, 'r') as f:
        for line in f:
            url_list.append(line.strip())

    return url_list


class Timer():
    def __init__(self):
        self.val = 0

    def tick(self):
        self.val = time.time()

    def tock(self):
        return round(time.time() - self.val, 6)

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.进度条.py
# @Author:Mysticat

import time

# import progressbar
# p = progressbar.ProgressBar()
# # # 假设需要执行100个任务，放到ProgressBar()中
# for i in p(range(100)):
#     """
#     代码
#     """
#     # 假设这代码部分需要0.05s
#     time.sleep(0.05)
#


from tqdm import tqdm
for i in tqdm(range(1, 60)):
    """
    代码
    """
    # 假设这代码部分需要0.05s，循环执行60次
    time.sleep(0.05)


#

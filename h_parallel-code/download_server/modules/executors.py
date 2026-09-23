#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :executors.py
# @Author:Mysticat


# 线程池模块
# 进程池模块
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

MULTI_NUMS = 10

thread_pool_executor = ThreadPoolExecutor(MULTI_NUMS)
process_pool_executor = ProcessPoolExecutor(MULTI_NUMS)




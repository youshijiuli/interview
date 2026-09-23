#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test04.py
# @Author:Mysticat


import os
import time
from multiprocessing import set_start_method
from concurrent.futures import ProcessPoolExecutor

set_start_method('fork')


def task(i):
    print(f'正在执行任务{i + 1}')
    time.sleep(1)



pool = ProcessPoolExecutor(4)

for i in range(10):
    pool.submit(task,i)

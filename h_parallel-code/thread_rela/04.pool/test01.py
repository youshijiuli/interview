#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.sleep.py
# @Author:Mysticat

import time
# from concurrent.futures import ThreadPoolExecutor
import concurrent.futures


def task(index):
    print(f'task{index} starting...')
    time.sleep(1)
    print(f'task{index} ending...')


start = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    futures = [
        pool.submit(task, i) for i in range(10)
    ]

# 等待所有线程完成

concurrent.futures.wait(futures)

print(f'cost time {time.time() - start}')

print('over ...')

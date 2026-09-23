#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.sleep.py
# @Author:Mysticat

import os
import time
import random
from multiprocessing import Pool


def long_time_task(name):
    """
    打印每条进程的随机运行时间
    :param name:
    :return:
    """
    print(f'run task {name} on subprocess({os.getpid()})...')
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print(f'task {name} runs {end - start:0.2f} seconds.')


if __name__ == '__main__':
    print(f'paren process {os.getpid()}')
    pool = Pool(10)
    for i in range(50):
        pool.apply_async(
            long_time_task, args=(i + 1,)
        )
    print('waiting for all subprocesses done...')
    # 先关闭进程池；此时pool中的子进程未必已结束，但是池子不再接受新任务
    pool.close()
    # 再阻塞主进程，等待进程中的子进程全部结束
    pool.join()
    print('all subprocesses done.')

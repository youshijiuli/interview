#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.yield_from.py
# @Author:Mysticat


import os
import time
import random
import multiprocessing


def func(name):
    print(f'进程{name}启动>pid-{os.getpid()} {time.time()}')
    brgin = time.time()
    time.sleep(random.choice([1, 2]))
    end = time.time()
    print(f'进程{name}结束>用时:{end - brgin} {time.time()}')


if __name__ == '__main__':
    print('主进程启动>PID-%s %s' % (os.getppid(), time.ctime()))

    # 创建进程池
    # Pool()参数不写默认大小是CPU核心数
    pool = multiprocessing.Pool(5)
    for i in range(1, 21):
        # process_pool = multiprocessing.Process(target=func, args=(i, ))
        # 放入进程池统一管理
        # 异步方式执行，所有进程同时执行
        pool.apply_async(func, args=(i,))

        # 同步执行，一个进程执行完另一个进程执行
        # 同步方式不需要close 和 join
        # process_pool.apply(func, args=(i, ))

    # 在调用join之前必须调用close，调用close之后不能再添加新的进程了
    pool.close()
    pool.join()

    print('主进程over')

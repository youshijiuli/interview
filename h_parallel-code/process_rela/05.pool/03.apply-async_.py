#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.apply-async_.py
# @Author:Mysticat
import os

import time
from multiprocessing import Pool


def worker(msg):
    t_start = time.time()
    print(f'{msg}开始执行，进程号码为：{os.getpid()}')
    time.sleep(2)
    t_stop = time.time()
    print(msg, f'执行完成，耗时{t_stop - t_start}')

if __name__ == '__main__':
    pool = Pool(5)
    for i in range(10):
        pool.apply_async(worker,(i+1,))
    print('main start') # 最开始打印

    pool.close()

    # 关闭进程池 在添加 进程任务 运行报错
    # po.apply_async(worker)  # Pool not running

    # 执行完子进程 再执行主进程
    pool.join()



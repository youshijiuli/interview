#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :10.pool_use_queue.py
# @Author:Mysticat


import os, time
from multiprocessing import Manager, Pool


def writer(q):
    print(f'写入进程启动，id:{os.getpid()}')
    for i in 'abcdefg':
        q.put(i)


def reader(q):
    print(f'读取进程启动，id:{os.getpid()}')
    for i in range(q.qsize()):
        print(i, '...')


if __name__ == '__main__':
    q = Manager().Queue()
    pool = Pool()
    pool.apply_async(writer, (q,))
    time.sleep(5)
    pool.apply_async(reader, (q,))
    pool.close()
    pool.join()

    print('over.....')

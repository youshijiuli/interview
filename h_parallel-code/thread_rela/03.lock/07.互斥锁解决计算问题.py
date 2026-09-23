#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :07.互斥锁解决计算问题.py
# @Author:Mysticat


"""
之前的计算错误问题是因为计算步骤缺失导致了计算误差
所以只要保证计算步骤都完整性就可以解决问题
"""

import time
import threading

g_num = 0

mutex = threading.Lock()


def test1(num):
    global g_num
    mutex.acquire()

    for _ in range(num):
        g_num += 1


    mutex.release()

    print(f'test1中的num={g_num}')


def test2(num):
    global g_num
    mutex.acquire()

    for _ in range(num):
        g_num += 1

    mutex.release()
    print(f'test2中的num={g_num}')


if __name__ == '__main__':
    t1 = threading.Thread(target=test1, args=(1000000,))
    t2 = threading.Thread(target=test2, args=(1000000,))

    t1.start()
    t2.start()

    time.sleep(1)
    print(g_num, 'main')

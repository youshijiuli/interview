#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.互斥锁.py
# @Author:Mysticat

import time
import threading

num = 100


def demo1(nums, mutex: threading.Lock):
    global num
    mutex.acquire()

    for _ in range(nums):
        num += 1

    mutex.release()
    print(f'demo1--{num}')


def demo2(nums, mutex: threading.Lock):
    global num
    mutex.acquire()

    for _ in range(nums):
        num += 1

    mutex.release()
    print(f'demo2--{num}')


if __name__ == '__main__':
    # 1.创建互斥锁对象
    mutex = threading.Lock()

    t1 = threading.Thread(target=demo1, args=(1000000, mutex))
    t2 = threading.Thread(target=demo2, args=(1000000, mutex))
    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print('main', num)


"""
demo1--1000100
demo2--2000100
main 2000100
"""
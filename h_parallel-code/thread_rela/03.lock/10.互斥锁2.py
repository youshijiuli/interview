#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :10.互斥锁2.py
# @Author:Mysticat


import time

from threading import Thread, Lock

num = 0


def demo1(nums: int, mutex: Lock):
    global num
    mutex.acquire()

    for _ in range(nums):
        num += 1

    mutex.release()

    print(f'demo1 -- {num}')


def demo2(nums: int, mutex: Lock):
    global num

    mutex.acquire()

    for _ in range(nums):
        num += 1

    mutex.release()

    print(f'demo2 -- {num}')


if __name__ == '__main__':
    mutex = Lock()

    t1 = Thread(target=demo1, args=(1000000, mutex))
    t2 = Thread(target=demo2, args=(1000000, mutex))
    t1.start()
    t2.start()

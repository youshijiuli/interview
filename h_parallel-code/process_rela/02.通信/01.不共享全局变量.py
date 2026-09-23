#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.不共享全局变量.py
# @Author:Mysticat


import time
import multiprocessing

# 进程之间不共享全局变量
num = 100


def demo1():
    global num
    num += 1

    print(f'demo1 -- {num}')


def demo2():
    time.sleep(3)
    print(f'demo2 -- {num}')


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=demo1)
    p2 = multiprocessing.Process(target=demo2)

    p1.start()
    p1.join()
    p2.start()


"""
demo1 -- 101
demo2 -- 100
"""
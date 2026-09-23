#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :06.共享1.py
# @Author:Mysticat


# 1. 没有使用global  那么函数内部只能访问全局变量；无法修改；
# 2. 全局变量共享；但是有可能由于线程执行顺序导致访问的时候还没有被修改；这个是很合理的


import threading

num = 100


def func1():
    global num
    num += 1
    print('func1', num)


def func2():
    print('func2', num)


if __name__ == '__main__':
    t1 = threading.Thread(target=func1)
    t2 = threading.Thread(target=func2)

    t1.start()
    t2.start()

    print('main over')
    """
    func1 101
    func2main over
    101
    """

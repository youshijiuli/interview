#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.easy.py
# @Author:Mysticat

import time


def func1():
    for i in range(5):
        print(f'第{i + 1}次,这是func1')
        i += 1
        time.sleep(2)
        yield


def func2():
    for i in range(5):
        print(f'第{i + 1}次：这是func2')
        i += 1
        time.sleep(0.2)
        yield


if __name__ == '__main__':
    f1 = func1()
    f2 = func2()
    try:
        while True:
            next(f1)
            next(f2)
    except StopIteration as e:
        print(e)

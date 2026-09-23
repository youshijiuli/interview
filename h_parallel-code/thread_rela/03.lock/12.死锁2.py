#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :12.死锁2.py
# @Author:Mysticat


import time

from threading import Thread, Lock


def func1():
    lock1.acquire()
    print('func1拿到菜刀')
    time.sleep(1)
    lock2.acquire()
    print('func1拿到锅子')
    lock2.release()
    print('func1释放锅子')
    lock1.release()
    print('func1释放锅子')


def func2():
    lock2.acquire()
    print('func2拿到锅子')
    lock1.acquire()
    print('func2拿到菜刀')
    lock1.release()
    print('func2释放菜刀')
    lock1.release()
    print('func2释放锅子')


if __name__ == '__main__':
    lock1 = Lock()
    lock2 = Lock()

    t1 = Thread(target=func1)
    t2 = Thread(target=func2)
    t1.start()
    t2.start()

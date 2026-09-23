#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.sleep.py
# @Author:Mysticat

from threading import Thread,Lock

lock = Lock()
n = 5000


def func1():
    global n
    for i in range(1000000):
        lock.acquire()
        n += 1
        lock.release()

def func2():
    global n
    for i in range(1000001):
        lock.acquire()
        n -= 1
        lock.release()

if __name__ == '__main__':
    t1 = Thread(target=func1)
    t2 = Thread(target=func2)

    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(n)



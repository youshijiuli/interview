#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.信号.py
# @Author:Mysticat


import time
from threading import Semaphore, Thread


def home(name, sem):
    sem.acquire()
    print(f'{name}----进入房间')
    time.sleep(3)
    print(f'{name}---走出房间')
    sem.release()


if __name__ == '__main__':
    sem = Semaphore(5)

    for i in range(20):
        t = Thread(target=home, args=(i + 1,sem))
        t.start()

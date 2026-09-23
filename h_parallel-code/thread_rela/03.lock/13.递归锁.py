#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :13.递归锁.py
# @Author:Mysticat


import time
import threading

num = 0

# lock = threading.Lock()  # 卡住
lock = threading.RLock()


def task():
    global num
    lock.acquire()
    num += 1
    lock.acquire()
    time.sleep(2)
    print(num)
    lock.release()
    lock.release()


for _ in range(10):
    t = threading.Thread(target=task)
    t.start()

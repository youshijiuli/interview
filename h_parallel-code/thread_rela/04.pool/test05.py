#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test05.py
# @Author:Mysticat

import threading
from concurrent.futures import ThreadPoolExecutor
import time


def action(max):
    my_sum = 0
    for i in range(max):
        my_sum += 1
        time.sleep(1)
    return my_sum


pool = ThreadPoolExecutor(5)

future1 = pool.submit(action, 10)
future2 = pool.submit(action, 20)

print(future1.done())
time.sleep(3)

print(future2.done())

print(future1.result())
print(future2.result())

pool.shutdown(True)


"""
False
False
10
20
"""
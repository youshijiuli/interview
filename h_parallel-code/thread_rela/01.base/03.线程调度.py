#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.线程调度.py
# @Author:Mysticat


import threading
import time

# condition中 acquire锁为递归锁，不会造成死锁
condition = threading.Condition()


def func1():
    with condition:
        for i in list('abcdefghij'):
            print(threading.current_thread().name, i)
            time.sleep(1)
            # 线程等待，func2执行
            condition.wait()
            condition.notify()
            # 传递信号，只能为整数，表示放行几个信号
            # condition.notify() # 全部


def func2():
    with condition:
        for i in range(10):
            print(threading.current_thread().name, i)
            time.sleep(1)
            # 线程执行
            condition.notify()
            # 执行完等待
            condition.wait()


if __name__ == '__main__':
    t1 = threading.Thread(target=func1)
    t1.start()
    t2 = threading.Thread(target=func2)
    t2.start()

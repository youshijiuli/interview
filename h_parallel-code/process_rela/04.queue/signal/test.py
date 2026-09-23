#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test.py
# @Author:Mysticat
import multiprocessing
import time
import random
from multiprocessing import Process,set_start_method


def semaphone(i, sem):
    sem.acquire()
    print("%d执行了" % i)
    time.sleep(random.randint(2, 5))
    print("%d执行完了" % i)
    sem.release()


if __name__ == '__main__':
    set_start_method('fork')
    # 每次只能有4个进程执行
    sem = multiprocessing.Semaphore(4)

    for i in range(20):
        p = multiprocessing.Process(
            target=semaphone,
            args=(i, sem)
        )
        p.start()

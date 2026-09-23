#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test03.py
# @Author:Mysticat

import time
from multiprocessing import Process, Queue


def write(queue):
    for value in list('abc'):
        queue.put(value)
        print(f"write:\t puts '{value}' into queue and sleeps 1 sec...")
        time.sleep(1)
        print("write:\t subprocess wakeup from sleeping.")


def read(queue):
    """
    从队列中读取数据的子进程
    :param queue:
    :return:
    """
    while True:
        print("read:\t waiting write subprocess...")
        value = queue.get()
        print(f"read:\t gets '{value}' from queue.")


if __name__ == '__main__':
    queue = Queue()
    pwrite = Process(target=write, args=(queue,))
    pread = Process(target=read, args=(queue,))
    pwrite.start()
    pread.start()
    pwrite.join()
    print('write finished!!!')
    pread.terminate()  # #pread子进程是个死循环，无法等待其结束，只能强行终止
    print('read:\t subprocess has been terminated.')

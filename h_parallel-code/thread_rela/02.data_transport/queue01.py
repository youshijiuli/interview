#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :queue01.py
# @Author:Mysticat

from queue import Queue
from threading import Thread
import time


def producer(queue:Queue):
    num = 1
    while True:
        if queue.qsize() < 8:
            print(f'生产{num}号馒头')
            queue.put(f'馒头{num}号')
            num += 1

        else:
            print("馒头框满了，等待来人消费啊！")
            time.sleep(1)

def comsumer(queue:Queue):
    while True:
        print(f"获取馒头：{queue.get()}")
        time.sleep(1)

if __name__ == '__main__':
    queue = Queue()
    t1 = Thread(target=producer,args=(queue,))
    t2 = Thread(target=comsumer,args=(queue,))
    t1.start()
    t2.start()



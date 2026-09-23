#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test03.py
# @Author:Mysticat

import queue
import time
from threading import Thread
from queue import Queue

#  此队列，先进先出

def producer(queue:Queue):
    num = 1
    while not queue.full():
        print(f'生产{num}号包子')
        queue.put({'id':num})
        num += 1
        time.sleep(.5)
    print('满了，满了')

def consumer(queue:Queue):
    while not queue.empty():
        print(f"获取馒头：{queue.get()}")
        time.sleep(1)

if __name__ == '__main__':
    queue = Queue(10)
    t1 = Thread(target=producer,args=(queue,))
    t2 = Thread(target=consumer,args=(queue,))
    t1.start()
    t2.start()



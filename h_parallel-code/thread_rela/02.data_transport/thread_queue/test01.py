#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.test.py
# @Author:Mysticat
import threading
from queue import Queue
from threading import Thread
from time import sleep


def producer(queue: Queue):
    num = 1
    while True:
        if queue.qsize() < 5:
            print(f'生产{num}号馒头')
            queue.put({'item': f'馒头{num}号'})
            num += 1
        else:
            print('馒头框满了，等待来人消费啊！')
        sleep(1)


def consumer(queue: Queue):
    while True:
        print(f"获取馒头：{queue.get()}")
        sleep(1.5)


if __name__ == '__main__':
    queue = Queue()
    t1 = threading.Thread(target=producer, args=(queue,))
    t2 = threading.Thread(target=consumer, args=(queue,))
    t1.start()
    t2.start()

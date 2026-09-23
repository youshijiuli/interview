#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.demo.py
# @Author:Mysticat

import time
import threading
import queue
import random


class Producer(threading.Thread):
    def __init__(self,i,q):
        super().__init__()
        self.data = q
        self.i = i

    def run(self):
        while True:
            num = random.randint(1,10000)
            self.data.put(num)
            print("生产者%d生产了%d个数据" % (self.i, num))
            time.sleep(2)


class Consumer(threading.Thread):
    def __init__(self,j,q):
        super().__init__()
        self.data = q
        self.j = j

    def run(self):
        while True:
            get_num = self.data.get()
            print("消费者%d消费了%d个数据" % (self.j, get_num))
            time.sleep(3)


def main():
    q = queue.Queue()
    for i in range(5):
        p = Producer(i,q)
        p.start()

    for j in range(5):
        c = Consumer(j,q)
        c.start()


if __name__ == '__main__':
    main()
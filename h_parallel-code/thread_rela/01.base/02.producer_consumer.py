#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.producer_consumer.py
# @Author:Mysticat

import queue
import time
import threading
import random


def producer(i, q: queue.Queue):
    while True:
        num = random.randint(1, 10000)
        q.put(num)
        print("生产者%d生产了%d个数据" % (i, num))
        time.sleep(1)


def consumer(j, q: queue.Queue):
    while True:
        num_get = q.get()
        if not num_get:
            break
        print("消费者%d消费了%d个数据" % (j, num_get))
        time.sleep(2)


if __name__ == '__main__':
    q = queue.Queue()

    for i in range(3):
        p = threading.Thread(
            target=producer, args=(
                i, q
            )
        )

        p.start()

    for j in range(4):
        c = threading.Thread(
            target=consumer,
            args=(j, q)
        )

        c.start()


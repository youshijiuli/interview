#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :comsumer_producr.py
# @Author:Mysticat

import time
from threading import Thread
from queue import Queue


def producer(q, name):
    """
    生产者
    :return:
    """
    time.sleep(0.5)
    data = f'包子{name}号'
    q.put(data)
    print('%s生产了一个%s' % (name, data))


def consumer(q,name):
    while True:
        data = q.get()
        if not data:break
        time.sleep(0.5)
        print('%s吃了一个%s' % (name, data))

if __name__ == '__main__':
    q = Queue()
    p1 = Thread(target=producer, args=(q, '大壮'))
    p2 = Thread(target=producer, args=(q, 'egon'))
    c1 = Thread(target=consumer, args=(q, 'alex'))
    c2 = Thread(target=consumer, args=(q, '太白'))
    p1.start()
    c1.start()
    p2.start()
    c2.start()
    p1.join()
    p2.join()
    q.put(None)
    q.put(None)

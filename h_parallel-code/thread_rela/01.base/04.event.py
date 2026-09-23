#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :04.event.py
# @Author:Mysticat

import random
import time
from threading import Thread, Event

e = Event()


def conn():
    """测试链接"""
    count = 1
    while not e.is_set():
        print("尝试第{}次连接".format(count))
        if count > 4:
            raise TimeoutError
        count += 1
        e.wait(random.uniform(0.5, 2))

    if e.is_set():
        print('链接成功！！！')


def check_conn():
    """
    检查链接
    :return:
    """
    time.sleep(random.uniform(0.5, 2))
    e.set()


if __name__ == '__main__':
    t1 = Thread(target=conn)
    t1.start()
    t2 = Thread(target=check_conn)
    t2.start()

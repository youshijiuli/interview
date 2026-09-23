#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.事件.py
# @Author:Mysticat


import time
import threading


def chihuoguo(name):
    print(f'{name} -- start...')
    time.sleep(1)
    event.wait()
    print(f'{name} -- over...')


if __name__ == '__main__':
    event = threading.Event()
    t1 = threading.Thread(target=chihuoguo, args=('tom',))
    t2 = threading.Thread(target=chihuoguo, args=('jack',))

    t1.start()
    t2.start()

    # 上面在event.wait夯住，必须接受事件通知
    time.sleep(1)
    event.set()

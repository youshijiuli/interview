#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :04.gevent_base.py
# @Author:Mysticat


import gevent

def func():
    for i in range(5):
        print(gevent.getcurrent(),f'第{i+1}次执行')
        # # 用来模拟一个耗时操作，注意不是time模块中的sleep
        # # 没有gevent的sleep耗时，每个协程会一次执行
        # # 有耗时，则会依次每个协程执行一次再次循环
        gevent.sleep(1)


g1 = gevent.spawn(func)
g2 = gevent.spawn(func)
g3 = gevent.spawn(func)


g1.join()
g2.join()
g3.join()

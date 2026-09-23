#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.gevent.py
# @Author:Mysticat


import time
import gevent
from gevent import monkey


# 打补丁，gevent框架识别耗时操作，比如：time.sleep，网络请求延时.
# 需在程序前面
monkey.patch_all()


def func1(n):
    for i in range(n):
        print(f'第{i + 1}次：这是func1')
        i += 1
        # time.sleep(0.2)  # 如果没有猴子补丁，此耗时操作无用
        gevent.sleep(0.2)


def func2(n):
    for i in range(n):
        print(f'第{i + 1}次：这是func2')
        i += 1
        # time.sleep(0.2)  # 如果没有猴子补丁，此耗时操作无用
        gevent.sleep(0.2)


g1 = gevent.spawn(func1,5)
g2 = gevent.spawn(func2,5)



# # 主线程等待协程执行完成以后程序再退出
# g1.join()
# g2.join()

# 可以使用joinall(),参数为对象,需以列表形式传入
# gevent.joinall([g1, g2])

# 如果程序本身是一个死循环，且有耗时操作，就不需要使用join方法了
# while True:
#
#     print('主线程')
#     time.sleep(0.2)

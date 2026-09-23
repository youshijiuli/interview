#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :08.回调.py
# @Author:Mysticat

import os
import time
from concurrent.futures import ProcessPoolExecutor



# pool = ThreadPoolExecutor(5)  # 池子里面固定只有五个线程
# 括号内可以传数字 不传的话默认会开设当前计算机cpu个数五倍的线程
pool = ProcessPoolExecutor(5)
# 括号内可以传数字 不传的话默认会开设当前计算机cpu个数进程

"""
池子造出来之后 里面会固定存在五个线程
这个五个线程不会出现重复创建和销毁的过程
池子造出来之后 里面会固定的几个进程
这个几个进程不会出现重复创建和销毁的过程

池子的使用非常的简单
你只需要将需要做的任务往池子中提交即可 自动会有人来服务你
"""


def task(n):
    print(n,os.getpid())
    time.sleep(2)
    return n**2


def callback(n):
    print('call_back>>>:', n.result())


"""
任务的提交方式
    同步:提交任务之后原地等待任务的返回结果 期间不做任何事
    异步:提交任务之后不等待任务的返回结果 执行继续往下执行
        返回结果如何获取？？？
        异步提交任务的返回结果 应该通过回调机制来获取
        回调机制
            就相当于给每个异步任务绑定了一个定时炸弹
            一旦该任务有结果立刻触发爆炸
"""

if __name__ == '__main__':
    # pool.submit(task, 1)  # 朝池子中提交任务  异步提交
    # print('主')
    t_list = []
    for i in range(20):  # 朝池子中提交20个任务
        # res = pool.submit(task, i)  # <Future at 0x100f97b38 state=running>
        res = pool.submit(task, i).add_done_callback(callback)
        # print(res.result())  # result方法   同步提交
        # t_list.append(res)
    # 等待线程池中所有的任务执行完毕之后再继续往下执行
    # pool.shutdown()  # 关闭线程池  等待线程池中所有的任务运行完毕
    # for t in t_list:
    #     print('>>>:',t.result())  # 肯定是有序的
"""
程序有并发变成了串行
任务的为什么打印的是None
res.result() 拿到的就是异步提交的任务的返回结果
"""

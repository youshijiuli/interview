#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test07.py
# @Author:Mysticat


# 开启一个线程池，提交执行200个任务，获取200个任务的返回值
import time, random
from threading import current_thread
from concurrent.futures import ThreadPoolExecutor


def task(a, b):
    print(current_thread().ident, 'start', a, b)
    time.sleep(3)
    print(current_thread().ident, 'end', a)
    return a, a * b


def get_result(res):
    print(res.result())


if __name__ == '__main__':
    pool = ThreadPoolExecutor(10)
    for i in range(200):
        ret = pool.submit(task, i, i + 1)
        ret.add_done_callback(get_result)



# 要等待这200个任务结束前后，在log⽂件中记录开始和结束事件（4分）


# import time, random
# from threading import current_thread
# from concurrent.futures import ThreadPoolExecutor
#
# def file(args):
#     with open('log1',mode='a',encoding='utf-8') as f:
#         f.write(args+'\n')
#
# def func(a, b):
#     print(current_thread().ident, 'start', a, b)
#     file('start')
#     time.sleep(random.randint(1, 4))
#     print(current_thread().ident, 'end', a)
#     file('end')
#     return (a, a * b)
#
#
# def print_func(ret):
#     print(ret.result())
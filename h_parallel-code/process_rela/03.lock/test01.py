#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.sleep.py
# @Author:Mysticat


import time
import json
import random
import multiprocessing

"""
多个进程共享同一个文件，我们可以把文件当成数据库，用多个进程来模拟人抢票的过程；db.json中的数据是：{"count": 3}
"""


def search():
    """查询剩余票数"""
    time.sleep(random.randint(1, 3))  # 模拟网络请求
    with open('db.json', 'rt', encoding='utf-8') as f:
        dic = json.load(f)
        print(f'{multiprocessing.current_process().name}剩余票数：{dic["count"]}')


def get():
    """购买车票，包括读取数据库、判断剩余票数是否足够、修改数据库、打印购票成功，这四个步骤是一个整体，应该全部置于锁内，模拟成一个原子操作"""
    time.sleep(random.randint(1, 3))  # 模拟网络延迟

    with open('db.json', 'rt', encoding='utf-8') as fin:
        dic = json.load(fin)

    if dic["count"] > 0:
        dic['count'] -= 1
        with open('db.json', 'wt', encoding='utf-8') as fout:
            json.dump(dic, fout)
        print(f'{multiprocessing.current_process().name}购票成功！！')

    else:
        print(f'{multiprocessing.current_process().name}购票失败，票已经卖完！！')


def task(lock):
    search()

    try:
        lock.acquire()
        get()
    except Exception as error:
        print(error)
    finally:
        lock.release()


if __name__ == '__main__':
    MUTEX_LOCK = multiprocessing.Lock()

    # 互斥锁和join的区别一：
    # 互斥锁可以让一部分代码（即修改共享数据的代码）串行，而join只能将代码整体串行
    for i in range(5):
        process = multiprocessing.Process(target=task, args=(MUTEX_LOCK,))
        process.start()

        process.join()

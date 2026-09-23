#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.sleep.py
# @Author:Mysticat


import time
from multiprocessing import Process, JoinableQueue


def washer(queue):
    """洗盘子的子进程"""
    for dish in ['salad', 'bread', 'entree', 'dessert']:
        print(f'washing {dish} dish')
        queue.put(dish)
        time.sleep(1)


def dryer(queue):
    """烘盘子"""
    while True:
        dish = queue.get()
        print(f'drying {dish} dish')
        time.sleep(2)
        # #每烘干一个盘子，通知队列一项任务被完成
        queue.task_done()


if __name__ == '__main__':
    queue = JoinableQueue()
    washer_process = Process(
        target=washer, args=(queue,)
    )
    dryer_process = Process(
        target=dryer, args=(queue,)
    )

    washer_process.start()
    dryer_process.start()
    # 在洗盘子子进程结束前，阻塞主进程
    washer_process.join()
    # #在队列中的所有任务都被完成前，阻塞主进程
    queue.join()
    dryer_process.terminate()
    print('all done')
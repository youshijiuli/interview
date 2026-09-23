#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test05.py
# @Author:Mysticat


from multiprocessing import Queue, Process,set_start_method
import time


def add(queue: Queue):
    for i in range(10):
        if queue.full():
            print('满了')
            break
        queue.put(i)
        print(f'{i}被放进队列了')
        time.sleep(.5)


def read(queue: Queue):
    while True:
        if queue.empty():
            print('空了')
            break
        value = queue.get()
        print(f'{value}被拿出来了')
        time.sleep(.5)


if __name__ == '__main__':
    set_start_method('fork')
    queue = Queue(5)
    add_process = Process(
        target=add, args=(queue,)
    )
    read_process = Process(
        target=read, args=(queue,)
    )

    add_process.start()
    # add_process.join()

    read_process.start()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.先进先出.py
# @Author:Mysticat


from queue import Queue

"""
队列：先进先出 （排队买奶茶）
栈：先进后出 (洗碗)
"""

from multiprocessing import Process, Queue,set_start_method


def download(q: Queue):
    for i in range(3):
        q.put(i)
    print('添加完毕')


def merge_data(q: Queue):
    manager_list = []
    while not q.empty():
        manager_list.append(q.get())

    print(manager_list)


if __name__ == '__main__':
    set_start_method('fork')
    q = Queue()
    p1 = Process(target=download, args=(q,))
    p2 = Process(target=merge_data, args=(q,))
    p1.start()
    p2.start()

    """
    添加完毕
    [0, 1, 2]
    """
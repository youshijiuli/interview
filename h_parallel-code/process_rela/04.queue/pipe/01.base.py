#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.base.py
# @Author:Mysticat

import time
from multiprocessing import Process, Pipe, current_process


def func1(conn1):
    sub_info = 'hello'
    print(f'{current_process().pid}发送数据：{sub_info}')
    time.sleep(1)
    conn1.send(sub_info)
    print(f'收到进程2的信息：{conn1.recv()}')
    time.sleep(1)


def func2(conn2):
    sub_info = 'world!'
    print(f'{current_process().pid}发送数据：{sub_info}')
    time.sleep(1)
    conn2.send(sub_info)
    print(f'收到进程1的信息：{conn2.recv()}')
    time.sleep(1)


if __name__ == '__main__':
    conn1, conn2 = Pipe()

    p1 = Process(target=func1, args=(conn1,))
    p2 = Process(target=func2, args=(conn2,))

    p1.start()
    p2.start()

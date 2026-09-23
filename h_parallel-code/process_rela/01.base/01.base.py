#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.base.py
# @Author:Mysticat


import os
from multiprocessing import Process


def task(arg):
    print(f'I am a proceee,my name is {arg} and I am runing')


if __name__ == '__main__':
    print(f'i am the main process of the following process! my id is {os.getpid()}')
    # 创建一个进程对象
    process = Process(target=task, args=('child',))
    # 开始运行子进程
    process.start()
    process.join()
    print('process is ending!!!')

    """
    i am the main process of the following process! my id is 46752
    I am a proceee,my name is child and I am runing
    process is ending!!!
    """
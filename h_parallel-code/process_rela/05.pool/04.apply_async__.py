#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :04.apply_async__.py
# @Author:Mysticat


import multiprocessing

def demo1(q):
    try:
        # 注意：进程池里面的进程，如果出现异常，并不会报出异常 而是阻塞
        q.put('a')
        print('--1--')
    except Exception as e:
        print(e)


def demo2(q):
    print(q.get())
    print('--2--')



if __name__ == '__main__':
    q = multiprocessing.Manager().Queue()
    # 2.进程池
    po = multiprocessing.Pool()

    # 3.添加任务
    po.apply_async(demo1, args=(q,))
    po.apply_async(demo2, args=(q,))

    po.close()
    po.join()

    """
    --1--
    a
    --2--
    """
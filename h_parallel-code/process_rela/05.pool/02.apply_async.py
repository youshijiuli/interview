#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.apply_async.py
# @Author:Mysticat


from multiprocessing import Pool
import os
from time import sleep


def func1(name):
    print(f"当前进程的ID:{os.getpid()},{name}")
    sleep(2)
    return name


def func2(args):
    print(args)


if __name__ == "__main__":
    pool = Pool(5)

    pool.apply_async(func=func1, args=('sxt1',), callback=func2)
    pool.apply_async(func=func1, args=('sxt2',), callback=func2)
    pool.apply_async(func=func1, args=('sxt3',), callback=func2)
    pool.apply_async(func=func1, args=('sxt4',))
    pool.apply_async(func=func1, args=('sxt5',))
    pool.apply_async(func=func1, args=('sxt6',))
    pool.apply_async(func=func1, args=('sxt7',))
    pool.apply_async(func=func1, args=('sxt8',))

    pool.close()
    pool.join()

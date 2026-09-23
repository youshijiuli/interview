#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.yield_from.py
# @Author:Mysticat

import threading
import time


lock = threading.Lock()


def func(index):
    print(f'子线程{index}start获取🔒')
    lock.acquire()
    print(f'子线程{index}get🔒')
    my_list = [3,6,8,1]

    if index >= len(my_list):
        print('越界下标注',index)
        # 当索引超过列表长度时，需要进行解锁，如果不进行解锁，则会造成死锁(程序未停止)
        # 因为已经获取到锁了，结果越界了，如果不释放，那么其他的线程就获取不了锁，就会夯住造成死锁
        lock.release()
        return


    value = my_list[index]
    print(value)
    # 解锁
    lock.release()


for i in range(30):
    func_thread = threading.Thread(target=func,args=(i,))
    func_thread.start()



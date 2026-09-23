#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :06.死锁.py
# @Author:Mysticat


import threading

lock = threading.Lock()


def func(index):
    lock.acquire()

    my_list = [3, 6, 8, 1]

    if index >= len(my_list):
        print('越界下标', index)
        # 当索引超过列表长度时，需要进行解锁，如果不进行解锁，则会造成死锁(程序未停止,夯住)
        lock.release()
        return

    value = my_list[index]
    print(f'正常下标：值为 {value}')
    lock.release()


for i in range(30):
    t = threading.Thread(
        target=func, args=(i,)
    )
    t.start()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.内存共享.py
# @Author:Mysticat

import multiprocessing


def worker(dictionary, key, item):
    dictionary[key] = item
    print(f"key = {key},item = {item}")


if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    dictionary = mgr.dict()
    jonbs = [
        multiprocessing.Process(
            target=worker, args=(dictionary, i, i ** 2)
        ) for i in range(10)
    ]

    for j in jonbs:
        j.start()
    for j in jonbs:
        j.join()

    print('results', dictionary)


"""
key = 1,item = 1
key = 0,item = 0
key = 2,item = 4
key = 3,item = 9
key = 9,item = 81
key = 5,item = 25
key = 6,item = 36
key = 4,item = 16
key = 8,item = 64
key = 7,item = 49
results {1: 1, 0: 0, 2: 4, 3: 9, 9: 81, 5: 25, 6: 36, 4: 16, 8: 64, 7: 49}
"""
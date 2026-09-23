#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.yield_from.py
# @Author:Mysticat


import time
import concurrent.futures


def task(args):
    time.sleep(3)
    print(f'runing..{args}')
    return 666,'success'


pool = concurrent.futures.ThreadPoolExecutor(10)


futures_list = []

start = time.time()

for i in range(30):
    result = pool.submit(task,i)
    futures_list.append(result)


pool.shutdown(True)

print(f'cost time:{time.time() - start}') # cost time:9.015757083892822

for item in futures_list:
    print(item,type(item),item.result())


# <Future at 0x107e98250 state=finished returned tuple> <class 'concurrent.futures._base.Future'> (666, 'success')
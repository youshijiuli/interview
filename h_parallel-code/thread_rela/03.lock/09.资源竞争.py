#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :09.资源竞争.py
# @Author:Mysticat


import threading
num = 100

def demo1(nums):
    global num


    for _ in range(nums):
        num += 1

    print(f'demo1 -- {num}')



def demo2(nums):
    global num

    for _ in range(nums):
        num += 1

    print(f'demo2 -- {num}')


if __name__ == '__main__':
    t1 = threading.Thread(target=demo1,args=(1000000,))
    t2 = threading.Thread(target=demo2,args=(1000000,))
    t1.start()
    t2.start()


"""

demo1 -- 1796057
demo2 -- 2000100


由资源竞争 --> 互斥锁解决此问题

"""
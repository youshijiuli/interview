#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :07.共享2.py
# @Author:Mysticat

import threading

g_num = 0

def test_1(num):
    global g_num
    for _ in range(num):
        g_num += 1
    print(f'test_1中的g_num = {g_num}')


def test_2(num):
    global g_num
    for i in range(num):
        g_num += 1
    print(f'test_2中的g_num = {g_num}')



if __name__ == '__main__':
    t1 = threading.Thread(target=test_1,args=(1000000,))
    t2 = threading.Thread(target=test_2,args=(1000000,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print('main ',g_num)

"""
test_1中的g_num = 1887534
test_2中的g_num = 2000000
main  2000000
"""



'''
线程1在去执行计算时得出的结果没有来得及赋值就进行了任务切换
会导致计算结果错误

如何解决？
    互斥锁
'''

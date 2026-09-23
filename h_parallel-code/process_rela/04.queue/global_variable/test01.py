#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.sleep.py
# @Author:Mysticat


# 全局变量不在多个进程中共享

import multiprocessing

g_sum = 0



def sum1():
    for _ in range(1000000):
        global g_sum
        g_sum += 1
    print(g_sum)


def sum2():
    for _ in range(1000000):
        global g_sum
        g_sum += 1
    print(g_sum)


if __name__ == '__main__':
    print(g_sum)

    sub_process1 = multiprocessing.Process(
        target=sum1
    )

    sub_process2 = multiprocessing.Process(
        target=sum2
    )

    sub_process1.start()
    sub_process1.join()

    sub_process2.start()
    sub_process2.join()

    print('done')


"""
0
1000000
1000000
done
"""
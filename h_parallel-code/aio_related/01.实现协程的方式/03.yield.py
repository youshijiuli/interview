#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.yield.py
# @Author:Mysticat
import time


# 只要函数里面有yield,就是一个生成器函数，

# def func1():
#     yield 1
#     yield from func2()
#     yield 2
#
#
# def func2():
#     yield 3
#     yield 4
#
#
# f1 = func1()
# for num in f1:
#     print(num)


# ============================

#
# def task1():
#     while True:
#         print('--1--')
#         time.sleep(0.1)
#         yield
#
#
#
# def task2():
#     while True:
#         print('--2--')
#         time.sleep(.1)
#         yield
#
#
# if __name__ == '__main__':
#     t1 = task1()
#     t2 = task2()
#
#     while True:
#         next(t1)
#         next(t2)





# yield_from_v2
"""
子生成器
"""
def generator_1():
    total = 0
    while True:
        x = yield
        print("加", x)   # 2
        if not x:        # 判断是否为None  为None  退出循环 否则 才去相加 避免 None与数值相加报错
            break
        total += x
    return total


"""
委派生成器
"""
def generator_2():
    while True:
        total = yield from generator_1()
        print("加和总数是：", total)


"""
调用方
"""
def main():
    # g1 = generator_1()
    # g1.send(None)
    # g1.send(2)
    # g1.send(3)
    # g1.send(None)

    g2 = generator_2()
    g2.send(None)
    g2.send(2)
    g2.send(3)
    g2.send(None)

if __name__ == '__main__':
    main()






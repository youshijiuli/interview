#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.yield_from.py
# @Author:Mysticat

from itertools import chain

alist = [1, 2, 3]
dic = {
    'name': 'lisa',
    'age': 18
}
# print(chain(alist, dic))  # <itertools.chain object at 0x1011f2da0>
# print(list(chain(alist, dic)))  # [1, 2, 3, 'name', 'age']
#
# for v in chain(alist, dic):
#     print(v)


# 参数：可迭代的对象-->传入多个 会打包为元组
# 返回值：chain对象 所以，可以强转列表 显示 或者 for循环
# 本质：调用__next__方法
# print(list(chain(lis,dic)))


# 使用yield from实现一样的功能


def my_chain(*args):
    for my_iterable in args:
        # 使用yield生成器实现
        # for v in my_iterable:
        #     yield v

        # yield from 替代了 for循环
        yield from my_iterable


for value in my_chain(alist, dic):
    print(value)



print('--------')
def ge_1(lis):
    yield lis

def ge_2(lis):
    yield from lis

for i in ge_1(alist):
    print(i)

for i in ge_2(alist):
    print(i)















# from greenlet import greenlet
#
#
# def func1():
#     print(1)
#     gr2.switch()
#     print(2)
#     gr2.switch()
#
#
# def func2():
#     print(3)
#     gr1.switch()
#     print(4)
#     gr1.switch()
#
#
# if __name__ == '__main__':
#     gr1 = greenlet(func1)
#     gr2 = greenlet(func2)
#     gr1.switch()

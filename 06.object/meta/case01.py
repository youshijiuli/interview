#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026-09-11 0:29
# @File    : case01.py
# @Software: PyCharm

"""

"""


# class MyMeta(type):
#     def __new__(cls, name, bases, dct):
#         print(f"Creating class {name}")
#         return super().__new__(cls, name, bases, dct)
#
#
# class MyClass(metaclass=MyMeta):
#     pass
#
#
# if __name__ == '__main__':
#     my_class = MyClass()


def func(lst=[]):
    lst.append(1)
    return lst

print(func())
print(func())
print(func())

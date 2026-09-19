#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026-09-14 0:27
# @File    : bibao1.py
# @Software: PyCharm

"""
1. 什么是闭包？

在函数内部再定义一个函数，并且这个函数用到了外边函数的变量，那么将这个函数以及用到的一些变量称之为闭包。

简单的说，如果在一个内部函数里，对在外部作用域（但不是在全局作用域）的变量进行引用，那么内部函数就被认为是闭包(closure)。来看一个简单的例子:



"""


def addx(x):
    def adder(y):
        return x + y

    return adder


c = addx(8)
print(type(c))
print(c.__name__)
c(10)  # 18

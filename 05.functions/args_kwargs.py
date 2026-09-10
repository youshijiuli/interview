#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026-09-05 23:39
# @File    : args_kwargs.py
# @Software: PyCharm

"""

"""


def foo(*args, **kwargs):
    print(args)
    print(kwargs)


# 第一种
foo(1, 2, 3)
foo(a=1, b=2)
# 第二种
foo(*[1, 2, 3])
foo(**dict(a=1, b=2))

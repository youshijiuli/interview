#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :05.greenlet.py
# @Author:Mysticat

import time
import greenlet


def func1():
    for i in range(5):
        print(f'第{i}次执行，func1')
        time.sleep(0.5)
        # 切换到func2
        gl2.switch()




def func2():
    for i in range(5):
        print(f'第{i}次执行，func2')
        time.sleep(0.5)
        # 切换到func1
        gl1.switch()


if __name__ == '__main__':
    gl1 = greenlet.greenlet(func1)
    gl2 = greenlet.greenlet(func2)

    gl1.switch()
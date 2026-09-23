#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :05.共享全局变量.py
# @Author:Mysticat

import threading

g_num = 0


def func1():
    global g_num
    for i in range(10000):
        g_num += 1
    print(g_num)


func2 = func1

sub_process1 = threading.Thread(target=func1)
sub_process2 = threading.Thread(target=func2)

sub_process1.start()
sub_process2.start()

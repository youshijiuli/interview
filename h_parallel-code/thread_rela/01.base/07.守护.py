#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :07.守护.py
# @Author:Mysticat


import time
import threading



"""
- 自然情况下主线程执行完毕，但是仍然会等待子线程结束，主线程才会结束。
- t.setDaemon(True)  保护主线程 不会等子线程结束
- t.join()  等待子线程结束完毕，主线程再继续执行
"""



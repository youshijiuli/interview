#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :const.py
# @Author:Mysticat

from enum import Enum

class CalcType(Enum):
    """计算类型
    """
    singleThread = 0
    MultiThread = 1
    MultiProcess = 2
    PyCoroutine = 3



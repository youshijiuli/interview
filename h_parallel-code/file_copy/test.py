#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test.py
# @Author:Mysticat

import os

file_path = './new'

if not os.path.exists(file_path):
    os.makedirs(file_path)

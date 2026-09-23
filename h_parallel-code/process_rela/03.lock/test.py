#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test.py
# @Author:Mysticat


import json

with open('db.json', 'r', encoding='utf-8') as f:
    dic = json.load(f)

print(dic, type(dic))

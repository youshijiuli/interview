#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.demo.base.py
# @Author:Mysticat

import struct

ret = struct.pack('i',100000)
print(ret)
print(struct.unpack('i', ret))
ret = struct.pack('i', 1)
print(ret)
ret = struct.pack('i', 5)
print(ret)
ret = struct.pack('i', 10)
print(ret)
ret = struct.pack('i', 50)
print(ret)
ret = struct.pack('i', 7863)
print(ret)
print(struct.unpack('i', ret))

"""
b'\xa0\x86\x01.demo\x00'
(100000,)
b'\x01.demo\x00\x00\x00'
b'\x05\x00\x00\x00'
b'\n\x00\x00\x00'
b'2\x00\x00\x00'
b'\xb7\x1e\x00\x00'
(7863,)
"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :encrupt.py
# @Author:Mysticat



import hashlib


def md5_salt_username(username:str,pwd:str):
    obj = hashlib.md5(username.encode('utf-8'))
    obj.update(pwd.encode('utf-8'))
    return obj.hexdigest()


if __name__ == '__main__':
    res = md5_salt_username('lisa','123')
    print(res) # e9803a706f81a40884b8aeafafb2cfd3
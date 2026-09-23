#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.test.py
# @Author:Mysticat


import asyncio


async def func():
    print('hello world!!!')
    response = await asyncio.sleep(2)
    print('over', response)


result = func()

loop = asyncio.get_event_loop()
loop.run_until_complete(result)

"""
hello world!!!
over None
"""
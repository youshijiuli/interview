#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.yield_.py
# @Author:Mysticat

import asyncio

# example01
# async def main():
#     print('hello')
#     await asyncio.sleep(2)
#     print('world!!')
#
#
# asyncio.run(main())


# import asyncio
# import time
#
#
# async def say_after(delay, what):
#     """二级被调协程"""
#     await asyncio.sleep(delay)
#     print(what)
#
#
# async def main():
#     """一级被调协程，用来驱动二级被调协程"""
#     print('start at', time.strftime("%X"))
#     await say_after(1, 'hello')
#     await say_after(2, 'world')
#     print('finished at', time.strftime('%X'))
#
#
# #run函数，用来驱动一级被调协程
# asyncio.run(main())

"""
start at 08:47:30
hello
world
finished at 08:47:33

"""

# create_task

import time
import asyncio


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    """将二级被调协程封装成task对象，然后驱动后者"""
    task1 = asyncio.create_task(
        say_after(1, 'hello')
    )
    task2 = asyncio.create_task(
        say_after(2, 'world')
    )
    print('start at', time.strftime('%X'))
    await task1
    await task2
    print('finished at', time.strftime('%X'))


asyncio.run(main())




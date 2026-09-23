#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :04.asyncio.py
# @Author:Mysticat


import asyncio


async def func1():
    print(1)
    await asyncio.sleep(2)
    print(2)


async def func2():
    print(3)
    await asyncio.sleep(2)
    print(4)

# TODO:为什么此处写create_task不行，ensure_future才可以？？？

tasks = [
    asyncio.ensure_future(func1()),
    asyncio.ensure_future(func2()),
]
# 注意：基于asyncio模块实现的协程比之前的要更厉害，因为他的内部还集成了遇到IO耗时操作自动切花的功能。
# Python3.8之后 `@asyncio.coroutine` 装饰器就会被移除，推荐使用async & awit 关键字实现协程代码。
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

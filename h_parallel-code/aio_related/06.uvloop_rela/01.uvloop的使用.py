#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.uvloop的使用.py
# @Author:Mysticat


import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def func():
    print(1)
    await asyncio.sleep(2)
    print(2)
    return 666


async def main():
    print('start...')
    # 创建task对象，将当前的func任务添加到事件循环中
    task1 = asyncio.create_task(func())
    task2 = asyncio.create_task(func())
    print('ending...')
    # 当执行某些协程遇到IO操作时，会自动切换执行其他任务
    # 此处的await是等待相对应的协程全部执行完毕并获取结果

    res1 = await task1
    res2 = await task2

    print(res1, res2) # 666 666


asyncio.run(main())

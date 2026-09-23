#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :04.task_.py
# @Author:Mysticat

import asyncio


async def func():
    print(1)
    await asyncio.sleep(2)
    print(2)
    return 'return value'


async def main():
    print('main start')
    # 创建Task对象 将当前的执行func函数执行到事件循环中
    task1 = asyncio.create_task(func())
    # 创建Task对象 将当前的执行func函数执行到事件循环中
    task2 = asyncio.create_task(func())
    print('main over')

    # 当执行协程遇到IO操作时, 会自动化切换执行其他任务
    # 此处的await是等待相对应的协程全都执行完毕并获取结果

    res1 = await task1
    res2 = await task2

    print(res1, res2)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# main start
# main over
# 1
# 1
# 2
# 2
# return value return value

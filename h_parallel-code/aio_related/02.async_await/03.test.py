#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.test.py
# @Author:Mysticat

import asyncio


async def others():
    print('start')
    await asyncio.sleep(2)
    print('end')
    return '返回值'


async def func():
    print('start func')
    # 遇到IO操作挂起当前协程(任务),等待IO操作完成之后再继续往下执行
    response = await others()
    print('over', response)

    # 遇到IO操作挂起当前协程(任务),等待IO操作完成之后再继续往下执行
    response = await others()
    print("over", response)


loop = asyncio.get_event_loop()
loop.run_until_complete(func())

# start func
# start
# end
# over 返回值
# start
# end
# over 返回值

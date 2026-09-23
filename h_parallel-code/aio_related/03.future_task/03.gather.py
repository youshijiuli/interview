#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.gather.py
# @Author:Mysticat

import time
import asyncio


async def func1():
    for i in range(3):
        print(f'北京，第{i}次打印')
        await asyncio.sleep(1)

    return 'func1执行完毕'


async def func2():
    for i in range(3):
        print(f'上海，第{i}次打印')
        await asyncio.sleep(1)
    return 'func2执行完毕'


async def main():
    res = await asyncio.gather(
        func1(), func2()
    )
    # await异步执行func1方法
    # 返回值为函数的返回值列表

    print(res)


asyncio.run(main())

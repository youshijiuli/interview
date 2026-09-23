#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.task.py
# @Author:Mysticat


import asyncio


async def factorial(number):
    f = 1
    for i in range(2, number + 1):
        await asyncio.sleep(1)
        f *= i

    print(f)


async def fibonacci(number):
    a, b = 0, 1
    for i in range(number):
        await asyncio.sleep(1)
        a, b = b, a + b


if __name__ == '__main__':
    tasks = [
        asyncio.Task(factorial(10)),
        asyncio.Task(factorial(15)),
    ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.wait(tasks)
    )
    loop.close()
    """
    3628800
    1307674368000
    """
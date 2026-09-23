#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.yield_from.py
# @Author:Mysticat


# test01
#
#
# import asyncio
#
#
# async def nested():
#     return 90
#
#
# async def main():
#     # nested()  # 这条语句啥也不会做
#     res = await nested()
#     print(res)  # #使用await驱动后，打印出90
#
#
# asyncio.run(main())


import asyncio


async def nested():
    return 90


async def main():
    # #封装成task，也能像await关键字一样，驱动协程对象
    task = asyncio.create_task(nested())
    print(task)
    # 等待task执行完毕，就像线程池的future.result()方法，或者线程对象的thread.join()方法，完成前会阻塞调用方？？这里await的作用就是“等待”，而非“驱动”了
    await task
    print(task)


asyncio.run(main())
"""
<Task pending name='Task-2' coro=<nested() running at /Users/mac/PycharmProjects/parallel_learn/aio_related/00.asyncio/02.yield_from.py:29>>
<Task finished name='Task-2' coro=<nested() done, defined at /Users/mac/PycharmProjects/parallel_learn/aio_related/00.asyncio/02.yield_from.py:29> result=90>

"""


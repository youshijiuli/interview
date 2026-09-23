#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.task.py
# @Author:Mysticat


# import asyncio
#
#
# async def func():
#     print(1)
#     await asyncio.sleep(1)
#     print(2)
#     return 'func'
#
#
# async def main():
#     print('main start')
#
#     task1 = asyncio.create_task(func())
#     task2 = asyncio.create_task(func())
#
#     print('main over')
#
#     # 当执行某协程遇到IO操作时，会自动化切换执行其他任务。
#     # 此处的await是等待相对应的协程全都执行完毕并获取结果
#
#     res1 = await task1
#     res2 = await task2
#
#     print(res1)
#     print(res2)
#
#
# asyncio.run(main())



# ============================================


import asyncio

async def func():
    print(1)
    await asyncio.sleep(1)
    print(2)


async def main():
    print('main start')

    task_list = [
        asyncio.create_task(func(),name='n1'),
        asyncio.create_task(func(), name='n2')
    ]

    print('main over')

    # 当执行某协程遇到IO操作时，会自动化切换执行其他任务。
    # 此处的await是等待相对应的协程全都执行完毕并获取结果
    done, pending = await asyncio.wait(task_list, timeout=None)
    # timeout=None 默认就是如此，等所有的完成


    print(done,pending)


asyncio.run(main())



# =================


# import asyncio
#
#
# async def func():
#     print(1)
#     await asyncio.sleep(1)
#     print(2)
#     return 111
#
#
# task_list = [
#     asyncio.create_task(func(),name='n1'),
#     asyncio.create_task(func(), name='n2')
# ]
#
# done,pending = asyncio.run(asyncio.wait(task_list))
# print(done)
# RuntimeError: no running event loop
# sys:1: RuntimeWarning: coroutine 'func' was never awaited

# 事件循环还没有创建


# import asyncio
#
#
# async def func():
#     print(1)
#     await asyncio.sleep(1)
#     print(2)
#     return 111
#
#
# task_list = [
#     func(),
#     func()
# ]
#
# done, pending = asyncio.run(asyncio.wait(task_list))
# print(done)



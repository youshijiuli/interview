#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test03.py
# @Author:Mysticat

# import asyncio
# import datetime
#
#
# async def display_date():
#     loop = asyncio.get_event_loop()  # 搜寻并返回当前正在运转的事件循环
#     end_time = loop.time() + 5.0
#     while True:
#         if loop.time() >= end_time:
#             break
#         print(datetime.datetime.now())
#         await asyncio.sleep(1)  # 每阻塞1秒，loop.time()的值就+1
#
#
# asyncio.run(display_date())


"""

计算阶乘的任务

"""
# import asyncio
#
#
# async def factorial(name, number):
#     fact = 1
#     for i in range(2, number + 1):
#         print(f'task {name}: computed factorial({i})...')
#         await asyncio.sleep(1)
#         fact *= i
#
#     print(f'task {name}: factorial({number})')
#     return fact
#
#
# async def main():
#     tasks = asyncio.gather(
#         factorial('A', 2),
#         factorial('B', 3),
#         factorial('C', 4)
#     )  # 返回一个协程对象
#
#     result = await tasks
#     print('aggregate list of returned values is:', result)
#
#
# asyncio.run(main())




# import asyncio
#
#
# async def eternity():
#     await asyncio.sleep(3600)
#     print('yay!')
#
#
# async def main():
#     try:
#         await asyncio.wait_for(eternity(), timeout=1.0)
#     except asyncio.TimeoutError as error:
#         print('timeout', error)





import asyncio
from pprint import pprint

async def do_some_work(x):
    """二级被调协程"""
    print(f'waiting asyncio.sleep({x})...')
    await asyncio.sleep(x)
    print(f'work{x} done')

async def main():
    """一级被调协程"""
    result = await asyncio.wait([do_some_work(1),
                                 do_some_work(3)])
    pprint(result)

asyncio.run(main())






import asyncio
from pprint import pprint

async def nested():
    """二级被调协程"""
    return 42

async def main():
    """一级被调协程"""
    task = asyncio.create_task(nested()) #封装成task，也能像await关键字一样，驱动协程对象
    pprint(asyncio.current_task())
    pprint(asyncio.all_tasks())
    await task

asyncio.run(main())


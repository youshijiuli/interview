#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.future.py
# @Author:Mysticat


# import asyncio
#
# """
# 1.获取事件循环
# 2.创建一个任务【future对象】，这个任务什么都不干。
# 3.等待任务的最终结果，没有结果则会一直等下去。
# """
#
# async def main():
#     loop = asyncio.get_event_loop()
#     future = loop.create_future()
#     await future
#
#
# asyncio.run(main())


#######################################################################


# import asyncio
#
#
# async def set_after(future):
#     await asyncio.sleep(2)
#     future.set_result('666')
#
#
# async def main():
#     loop = asyncio.get_event_loop()
#     # 创建一个任务（Future对象），没绑定任何行为，则这个任务永远不知道什么时候结束。
#     future = loop.create_future()
#     # 创建一个任务（Task对象），绑定了set_after函数，函数内部在2s之后，会给fut赋值。
#     # 即手动设置future任务的最终结果，那么fut就可以结束了。
#     await loop.create_task(set_after(future))
#     # 等待 Future对象获取 最终结果，否则一直等下去
#     data = await future
#     print(data) # 666
#
#
# asyncio.run(main())


#######################################################################
# import time
# import asyncio
# from concurrent.futures import Future
# from concurrent.futures.thread import ThreadPoolExecutor
# from concurrent.futures.process import ProcessPoolExecutor
#
#
# def func(value):
#     time.sleep(1)
#     print(value)
#
#
# pool = ThreadPoolExecutor(5)
#
# for i in range(10):
#     future = pool.submit(func, i)
#     print(future)



#######################################################################


import time
import asyncio


def func1():
    # 某个耗时操作
    time.sleep(2)
    return "SB"


async def main():
    loop = asyncio.get_running_loop()
    # 1. Run in the default loop's executor ( 默认ThreadPoolExecutor )
    # 第一步：内部会先调用 ThreadPoolExecutor 的 submit 方法去线程池中申请一个线程去执行func1函数，并返回一个concurrent.futures.Future对象
    # 第二步：调用asyncio.wrap_future将concurrent.futures.Future对象包装为asycio.Future对象。
    # 因为concurrent.futures.Future对象不支持await语法，所以需要包装为 asycio.Future对象 才能使用。
    fut = loop.run_in_executor(None, func1)
    result = await fut
    print('default thread pool', result)
    # 2. Run in a custom thread pool:
    # with concurrent.futures.ThreadPoolExecutor() as pool:
    #     result = await loop.run_in_executor(
    #         pool, func1)
    #     print('custom thread pool', result)
    # 3. Run in a custom process pool:
    # with concurrent.futures.ProcessPoolExecutor() as pool:
    #     result = await loop.run_in_executor(
    #         pool, func1)
    #     print('custom process pool', result)


asyncio.run(main())
# default thread pool SB




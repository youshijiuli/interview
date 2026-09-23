#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test05.py
# @Author:Mysticat


"""为future添加回调"""

import asyncio


async def do_some_work(x):
    """一个协程"""
    print(f'waiting asyncio.sleep({x})')
    await asyncio.sleep(x)


def done_callback(future):
    """被回调的函数"""
    print('done')


# 1.创建事件循环
loop = asyncio.get_event_loop()

# 2.将协程对象封装成future对象
futuer = asyncio.ensure_future(do_some_work(3))

# 3.#为future对象添加回调功能
futuer.add_done_callback(done_callback)

# 4.#通过事件循环调用future对象
loop.run_until_complete(futuer)

# loop=asyncio.get_event_loop() #创建事件循环
# futures=asyncio.gather(do_some_work(1), do_some_work(3))
# futures.add_done_callback(done_callback)
# loop.run_until_complete(futures) #gather()协程返回的聚合列表，会返回到它的驱动/调用方


import asyncio
import concurrent.futures


def blocking_io():
    with open('xxx.json', 'r') as f:
        data = f.read()


def cpu_bound():
    """可能会阻塞事件循环的CPU密集型函数，通常建议使用进程池来执行"""
    return sum(i * i for i in range(10 ** 7))


async def main():
    """一级被调协程"""
    loop = asyncio.get_running_loop()

    # 选项1：使用事件循环自动创建的executor（线程池还是进程池未知）
    result = await loop.run_in_executor(None, blocking_io)
    print('default thread pool', result)

    # 选项2：使用自定义的线程池
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, blocking_io)
        print('custom thread pool', result)

    # 选项3：使用自定义的进程池
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, cpu_bound)
        print('custon process pool', result)


asyncio.run(main())  # 最外层的调用方——事件循环

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :00.base.py
# @Author:Mysticat


import asyncio

# 定义一个任务

# async def demo():
#     print('start')
#     await asyncio.sleep(1)
#     print('end')
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(demo())


# 启动多个任务, 无返回值
# async def multi_Demo():
#     print('start')
#     await asyncio.sleep(1)
#     print('end')
#
#
# loop = asyncio.get_event_loop()
# wait_obj = asyncio.wait(
#     [multi_Demo(), multi_Demo(), multi_Demo()]
# )
# loop.run_until_complete(wait_obj)

"""
start
start
start
end
end
end
"""

# 启动多个任务, 有返回值

#
# async def multi_demo_with_return():
#     print('start')
#     await asyncio.sleep(1)
#     print('end')
#     return '123'
#
#
# loop = asyncio.get_event_loop()
# t1 = loop.create_task(multi_demo_with_return())
# t2 = loop.create_task(multi_demo_with_return())
# tasks = [t1, t2]
#
# # for t in tasks:
# #     print(t.result())
# # asyncio.exceptions.InvalidStateError: Result is not set.
#
# wait_obj = asyncio.wait([t1, t2])
# loop.run_until_complete(wait_obj)
#
# # 必须要等到任务完成才能获取返回值
# # for t in tasks:
# #     print(t.result())


# 谁先回来先取谁的结果

import asyncio
#
#
# async def demo(i):
#     print('start')
#     await asyncio.sleep(10 - i)
#     print('end')
#     return i, 123
#
#
# async def main():
#     task_list = []
#     for i in range(10):
#         task = asyncio.ensure_future(demo(i))
#         task_list.append(task)
#
#     for ret in asyncio.as_completed(task_list):
#         res = await ret
#         print(res)
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())


# start
# start
# start
# start
# start
# start
# start
# start
# start
# start
# end
# (9, 123)
# end
# (8, 123)
# end
# (7, 123)
# end
# (6, 123)
# end
# (5, 123)
# end
# (4, 123)
# end
# (3, 123)
# end
# (2, 123)
# end
# (1, 123)
# end
# (0, 123)


#
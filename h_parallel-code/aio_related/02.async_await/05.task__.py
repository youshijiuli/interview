#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :05.task__.py
# @Author:Mysticat

import asyncio


async def func():
    print(1)
    await asyncio.sleep(2)
    print(2)
    return 'return value'


async def main():
    print('main start')
    task_list = [
        asyncio.create_task(func(), name='a1'),
        asyncio.create_task(func(), name='a2')
    ]
    print('main over')

    # 当执行协程遇到IO操作时, 会自动化切换执行其他任务
    # 此处的await是等待相对应的协程全都执行完毕并获取结果
    # done 如果两个完成之后 就会放到 done中 set类型
    # timeout 等待 多少秒 pending 就是 等待没有完成的 默认值 是 None
    done, pending = await asyncio.wait(task_list, timeout=None)
    print(done)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

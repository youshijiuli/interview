#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :05.demo.py
# @Author:Mysticat


import asyncio

async def func():
    print("执行协程函数内部代码")
    # 遇到IO操作挂起当前协程（任务），等IO操作完成之后再继续往下执行。    # 当前协程挂起时，事件循环可以去执行其他协程（任务）。
    response = await asyncio.sleep(2)
    print("IO请求结束，结果为：", response)


asyncio.run(func())
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.sleep.py
# @Author:Mysticat
import asyncio

import aiohttp


async def main():
    print('hello')
    await asyncio.sleep(3) #  模拟网络请求
    print('world!!!')


asyncio.run(main())

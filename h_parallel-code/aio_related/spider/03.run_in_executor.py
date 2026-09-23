#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.run_in_executor.py
# @Author:Mysticat

import requests
import asyncio


async def main():
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(None,requests.get,'https://www.baidu.com')
    future2 = loop.run_in_executor(None,requests.get,'https://www.baidu.com')
    response1 = await future1
    response2 = await future2

    print(response1.status_code)
    print(response2.status_code)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

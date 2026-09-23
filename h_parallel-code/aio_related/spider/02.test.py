#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.test.py
# @Author:Mysticat

# 不支持异步的模块
import requests
import asyncio


async def download_image(url: str):
    # 发送网络请求，下载图片（遇到网络下载图片的IO请求，自动化切换到其他任务）
    print('开始下载', url)
    loop = asyncio.get_event_loop()
    # requests模块默认不支持异步操作，所以就使用线程池来配合实现了。
    future = loop.run_in_executor(None, requests.get, url)
    response = await future

    print('下载完成')
    file_name = url.rsplit('_')[-1]
    with open(file_name, 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    url_list = [
        'https://www3.autoimg.cn/newsdfs/g26/M02/35/A9/120x90_0_autohomecar__ChsEe12AXQ6AOOH_AAFocMs8nzU621.jpg',
        'https://www2.autoimg.cn/newsdfs/g30/M01/3C/E2/120x90_0_autohomecar__ChcCSV2BBICAUntfAADjJFd6800429.jpg',
        'https://www3.autoimg.cn/newsdfs/g26/M0B/3C/65/120x90_0_autohomecar__ChcCP12BFCmAIO83AAGq7vK0sGY193.jpg'
    ]

    # TypeError: Passing coroutines is forbidden, use tasks explicitly.

    # 这个错误提示是因为在Python
    # 3.5
    # 及更高版本中，协程（coroutine）和任务（task）是两种不同的并发执行方式。当你尝试将协程传递给其他函数时，会收到这个错误。
    # 要解决这个问题，你需要显式地使用asyncio.create_task()
    # 或asyncio.ensure_future()
    # 来创建任务。

    # tasks = [asyncio.create_task(download_image(url)) for url in url_list]
    tasks = [asyncio.ensure_future(download_image(url)) for url in url_list]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

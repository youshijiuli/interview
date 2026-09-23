#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.sync_download.py
# @Author:Mysticat

# 同步下载

import requests

#
# def download_image(url: str):
#     print('开始下载', url)
#     response = requests.get(url)
#     name = url.rsplit('_')[-1]
#     with open(name, 'wb') as f:
#         f.write(response.content)
#
#     print(f'{name}下载完成')
#
#
# if __name__ == '__main__':
#     url_list = [
#         'https://www3.autoimg.cn/newsdfs/g26/M02/35/A9/120x90_0_autohomecar__ChsEe12AXQ6AOOH_AAFocMs8nzU621.jpg',
#         'https://www2.autoimg.cn/newsdfs/g30/M01/3C/E2/120x90_0_autohomecar__ChcCSV2BBICAUntfAADjJFd6800429.jpg',
#         'https://www3.autoimg.cn/newsdfs/g26/M0B/3C/65/120x90_0_autohomecar__ChcCP12BFCmAIO83AAGq7vK0sGY193.jpg']
#     for item in url_list:
#         download_image(item)


import aiohttp
import asyncio


async def fetch(session, url: str):
    print('开始下载', url)
    async with session.get(url, verify_ssl=False) as response:
        res = await response.content.read()
        file_name = url.rsplit('_')[-1]
        with open(file_name, 'wb') as file_obj:
            file_obj.write(res)
            print(f'{file_name}下载完成')


async def main():
    async with aiohttp.ClientSession() as seesion:
        url_list = [
            'https://www3.autoimg.cn/newsdfs/g26/M02/35/A9/120x90_0_autohomecar__ChsEe12AXQ6AOOH_AAFocMs8nzU621.jpg',
            'https://www2.autoimg.cn/newsdfs/g30/M01/3C/E2/120x90_0_autohomecar__ChcCSV2BBICAUntfAADjJFd6800429.jpg',
            'https://www3.autoimg.cn/newsdfs/g26/M0B/3C/65/120x90_0_autohomecar__ChcCP12BFCmAIO83AAGq7vK0sGY193.jpg']

        tasks = [
            asyncio.create_task(fetch(seesion, url)) for url in url_list
        ]

        await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())

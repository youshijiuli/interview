#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.download.py
# @Author:Mysticat


import time
import aiohttp
import asyncio


async def download_site(session, url):
    async with session.get(url) as response:
        print(f'read {response.content_length} from {url}')


async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(
                download_site(session, url)
            )
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)



if __name__ == '__main__':
    sites = [
                "https://www.jython.org",
                "http://olympus.realpython.org/dice",
            ] * 80

    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        download_all_sites(sites)
    )

    duration = time.time() - start
    print(f"Downloaded {len(sites)} sites in {duration} seconds")

    # Downloaded 160 sites in 28.355334043502808 seconds
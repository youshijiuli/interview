#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :04.thread_pool.py
# @Author:Mysticat

import blog_spider
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor(10) as pool:
    htmls = pool.map(blog_spider.craw, blog_spider.urls)
    htmls = list(zip(blog_spider.urls, htmls))
    for (url, html) in htmls:
        print(url, len(html))


print('crawl over')


# parse

with concurrent.futures.ThreadPoolExecutor(10) as pool:
    futures = {}
    for url,html in htmls:
        future = pool.submit(blog_spider.parse,html)
        futures[future] = url

    # for future, url in futures.items():
    # 	print(url, future.result())

    for future in concurrent.futures.as_completed(futures):
        url =futures[future]
        print(url,future.result())

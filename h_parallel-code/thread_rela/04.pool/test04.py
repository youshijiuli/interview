#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test04.py
# @Author:Mysticat


# 返回值回调函数

import time
from concurrent.futures import ThreadPoolExecutor


def get_html(url):
    time.sleep(1)
    print(f'get page {url} finnished')
    return {'state': 'done', 'url': url}


def callback(args):
    res = args.result()
    print(res)


with ThreadPoolExecutor(3) as pool:
    for i in range(10):
        result = pool.submit(get_html, f'www.xx{i}.com')
        result.add_done_callback(callback)

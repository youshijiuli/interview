#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.multi_thread.py
# @Author:Mysticat


import time
import threading
import blog_spider


def single_thread():
    print('single thread begin')
    for url in blog_spider.urls:
        blog_spider.craw(url)
    print('single_thread end')


def multi_thread():
    print('multi_thread begin')
    threads = []

    for url in blog_spider.urls:
        threads.append(
            threading.Thread(target=blog_spider.craw, args=(url,))
        )

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    start = time.time()
    single_thread()
    end = time.time()
    print("single_thread time", end - start)

    start = time.time()
    multi_thread()
    end = time.time()
    print("multi_thread time", end - start)

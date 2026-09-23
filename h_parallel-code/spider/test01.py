#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.sleep.py
# @Author:Mysticat

import requests
from lxml import etree
from urllib import request
import os, re
from queue import Queue
import threading

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


class Producer(threading.Thread):
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self) -> None:
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            # 解析页面，把img_path扔到img_queue
            self.parse_page(url)

    def parse_page(self, url):
        response = requests.get(url, headers=headers)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='random_article']//img/@src")
        for img in imgs:
            # img_url = img.get()
            img_url = img.get('data-original')
            alt = img.get('alt')
            alt = re.sub(r'[，。？?,/\\·]', '', alt)
            suffix = os.path.splitext(img_url)[1]
            suffix = re.sub(r'[!dta]', "", suffix)
            filename = alt + suffix
            # request.urlretrieve(img_url, 'images/' + filename)
            self.img_queue.put((img_url, filename))


class Consumer(threading.Thread):
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self) -> None:
        while True:
            if self.img_queue.empty():
                pass
            # img队列里面有数据，拿数据保存
            img_url, filename = self.img_queue.get()
            request.urlretrieve(img_url, f'./images/{filename}')
            print(filename + ' 下载完成')


def main():
    page_queue = Queue(100)
    img_queue = Queue(2000)

    for x in range(1, 10):
        # https://www.doutupk.com/article/list/?page=3
        url = "http://www.doutula.com/photo/list/?page=%d" % x
        page_queue.put(url)

    for x in range(5):
        t = Producer(page_queue, img_queue)
        t.start()

    for x in range(5):
        t = Consumer(page_queue, img_queue)
        t.start()


if __name__ == '__main__':
    main()

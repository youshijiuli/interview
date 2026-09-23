#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :blog_spider1.py
# @Author:Mysticat


import requests
from bs4 import BeautifulSoup

urls = [
    f"https://www.cnblogs.com/sitehome/p/{page}" for page in range(1, 10 + 1)
]

# print(urls[2])
#
# input('========')


def craw(url):
    r = requests.get(url)
    return r.text


def parse(html):
    # class="post-item-title"
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="post-item-title")
    return [(link["href"], link.get_text()) for link in links]


if __name__ == "__main__":
    for result in parse(craw(urls[2])):
        print(result)


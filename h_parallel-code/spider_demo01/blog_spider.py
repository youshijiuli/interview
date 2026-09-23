#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :blog_spider.py
# @Author:Mysticat


import requests
from bs4 import BeautifulSoup

# urls存储爬取页面的url, 以f开头表示在字符串内支持大括号内的python表达式
urls = [f"https://www.cnblogs.com/#p{page}" for page in range(1, 11)]


# 爬取函数
def craw(url: str):
    r = requests.get(url)
    return r.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    # links = soup.find_all("a", "post-item-title")
    # 当html 文档需要获取对应的css属性对应的标签的时候这个时候可以使用 css属性名字_= "属性值"的方式
    links = soup.find_all("a", class_="post-item-title")
    return [(link["href"], link.get_text()) for link in links]
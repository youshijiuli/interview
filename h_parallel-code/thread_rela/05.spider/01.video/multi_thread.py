#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :multi_thread.py
# @Author:Mysticat



import time
import requests
from threading import Thread

url_list = [
    ("东北F4模仿秀.mp4", "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0300f570000bvbmace0gvch7lo53oog"),
    ("卡特扣篮.mp4", "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200f3e0000bv52fpn5t6p007e34q1g"),
    ("罗斯mvp.mp4", "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200f240000buuer5aa4tij4gv6ajqg")
]

start = time.time()


def download(name, url):
    res = requests.get(url)
    with open(name, 'wb') as f:
        f.write(res.content)
        print(f'{name}下载完毕！')


for item in url_list:
    t = Thread(target=download, args=(item[0], item[1],))
    t.start()
    t.join()

print(time.time() - start)
# 1.63472318649292

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :index.py
# @Author:Mysticat

import time

import requests

url_list = [
    ("东北F4模仿秀.mp4", "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0300f570000bvbmace0gvch7lo53oog"),
    ("卡特扣篮.mp4", "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200f3e0000bv52fpn5t6p007e34q1g"),
    ("罗斯mvp.mp4", "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200f240000buuer5aa4tij4gv6ajqg")
]


def download_video(name, url):
    result = requests.get(url)
    with open(name, 'wb') as f:
        f.write(result.content)

        print(f'{name}下载完毕')


if __name__ == '__main__':
    for name, url in url_list:
        download_video(name, url)

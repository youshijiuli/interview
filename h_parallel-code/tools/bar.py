#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :bar.py
# @Author:Mysticat


import requests
from tqdm import tqdm


def download_file(url, output_path):
    # 发送 GET 请求获取文件总大小
    response = requests.head(url)
    file_size = int(response.headers.get('content-length', 0))

    # 使用 stream=True 发送 GET 请求以实现分块下载
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # 使用 tqdm 创建进度条，并分块下载文件
    with open(output_path, 'wb') as file, tqdm(
            desc=output_path,
            total=file_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            # 写入文件并更新进度条
            file.write(data)
            progress_bar.update(len(data))


if __name__ == "__main__":
    MP4_url = 'https://video.pearvideo.com/mp4/third/20190203/cont-1514365-10426650-170229-hd.mp4'
    output_file = 'test.mp4'
    # file_url = 'https://example.com/your_file_url'  # 替换为要下载的文件链接
    # output_file = 'downloaded_file.ext'  # 替换为保存的文件名及扩展名

    download_file(MP4_url, output_file)
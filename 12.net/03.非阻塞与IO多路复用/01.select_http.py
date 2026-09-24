#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.select_http.py
# @Author:Mysticat


import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from urllib.parse import urlparse

selector = DefaultSelector()


class Fetcher():
    def get_url(self,url):
        self.url = url
        url = urlparse(url)
        self.host = url.netloc
        self.path = url.path
        self.data = b""
        if self.path == "":
            self.path = "/"

        # 建立socket连接
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(False)

        try:
            self.client.connect((self.host, 80))
        except BlockingIOError as e:
            print(e)

        # 注册
        selector.register(self.client.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key):
        selector.unregister(key.fd)
        self.client.send(
            "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(self.path, self.host).encode("utf-8"))
        selector.register(self.client.fileno(), EVENT_READ, self.readed)

    def readed(self, key):
        recv_data = self.client.recv(1024)
        if recv_data:
            self.data += recv_data
        else:
            selector.unregister(key.fd)
            data = self.data.decode("utf-8")
            html_data = data.split("\r\n\r\n")[1]
            print(html_data)
            self.client.close()
            # windows系统中

def loop():
    # 事件循环，不停的请求socket的状态病调用对应的回调函数。socket本身不支持register模式
    while True:
        ready = selector.select()
        for key, mask in ready:
            call_back = key.data
            call_back(key)

fecther = Fetcher()

fecther.get_url("https://www.baidu.com")
loop()


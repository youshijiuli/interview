from multiprocessing import Process, Queue
import requests

import re
import json
# 4.生产者消费者实现的爬虫的例子

def producer(q, url):
    response = requests.get(url)
    q.put(response.text)


def consumer(q):
    while True:
        s = q.get()
        if not s: break
        com = re.compile(
            '<div class="item">.*?<div class="pic">.*?<em .*?>(?P<id>\d+).*?<span class="title">(?P<title>.*?)</span>'
            '.*?<span class="rating_num" .*?>(?P<rating_num>.*?)</span>.*?<span>(?P<comment_num>.*?)评价</span>', re.S)
        ret = com.finditer(s)
        for i in ret:
            print({
                "id": i.group("id"),
                "title": i.group("title"),
                "rating_num": i.group("rating_num"),
                "comment_num": i.group("comment_num")}
            )


if __name__ == '__main__':
    count = 0
    q = Queue(3)
    p_l = []
    for i in range(10):
        url = 'https://movie.douban.com/top250?start=%s&filter=' % count
        count += 25
        p = Process(target=producer, args=(q, url,)).start()
        p_l.append(p)
        p = Process(target=consumer, args=(q,)).start()
    for p in p_l: p.join()
    q.put(None)

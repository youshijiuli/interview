#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test04.py
# @Author:Mysticat

from multiprocessing import Queue

# 创建队列，消息为5个
queue = Queue(5)

queue.put('1')
queue.put(900)
queue.put(None)
queue.put([1, 2, 3])
queue.put({'a': 1})

# 注意不能一下子添加多个数据

# 满了之后再去put就会报错
# 当队列消息已放满，再put()数据会等待
# queue.put(2323)
# 使用put_nowait()不等待，直接报错
# queue.put_nowait(2323)

print(queue.full())

# queue.put_nowait(123)

# print(queue.qsize())
print(queue._maxsize) # 5

# 获取队列消息

value = queue.get()
print(value) # 1

# 当队列消息get完后再次使用get会等待
v1 = queue.get()
v2 = queue.get()
v3 = queue.get()
print(v1)
print(v2)
print(v3)


# 再次执行一下代码会等待，只有队列put值后才会取
# 使用get_nowait()不等待，直接报错，不建议使用
# value = queue.get()
# value = queue.get_nowait()

print(queue.empty()) # False
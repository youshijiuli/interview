#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.互斥锁.py
# @Author:Mysticat


import json
import time
import random
import multiprocessing


# 买票  1.先查 2.再买

def search(i):
    # 文件操作读取票数
    with open('db.json', 'r', encoding='utf-8') as f:
        dic = json.load(f)

    print('用户%s查询余票：%s' % (i, dic.get('count')))
    # 字典取值不要用[]的形式 推荐使用get  你写的代码打死都不能报错！！！


def buy(i):
    with open('db.json', 'r', encoding='utf-8') as f:
        dic = json.load(f)

    # 模拟网络延迟
    time.sleep(2)
    if dic['count'] > 0:
        dic['count'] -= 1

        with open('db.json', 'w', encoding='utf-8') as f:
            json.dump(dic, f)
        print(f'用户{i}购票成功！！！')

    else:
        print(f'余票不足，用户{i}购票失败！！！')


# 整合两个函数

def run(i, mutex):
    search(i)

    # 买票操作数据，需要上锁
    mutex.acquire()

    buy(i)
    mutex.release()


if __name__ == '__main__':
    from multiprocessing import set_start_method

    set_start_method('fork')
    # 在主进程中生成一把锁 让所有的子进程抢 谁先抢到谁先买票
    mutex = multiprocessing.Lock()
    for i in range(1, 11):
        p = multiprocessing.Process(target=run, args=(i, mutex))
        p.start()


"""
扩展 行锁 表锁

注意：
	1.锁不要轻易的使用，容易造成死锁现象(我们写代码一般不会用到，都是内部封装好的)
	2.锁只在处理数据的部分加来保证数据安全(只在争抢数据的环节加锁处理即可) 
"""


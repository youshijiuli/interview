#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :05.回调函数.py
# @Author:Mysticat

import time
from multiprocessing import Pool


def func1(n):
    print('func1')
    time.sleep(2)
    return n ** 2


def func2(n):
    print('func2')
    time.sleep(2)
    print(n)


if __name__ == '__main__':
    p = Pool(5)
    # args里面的10给了func1，func1的返回值作为回调函数的参数给了callback对应的函数，不能直接给回调函数直接传参数，他只能是你任务函数func1的函数的返回值
    # for i in range(10,20): #如果是多个进程来执行任务，那么当所有子进程将结果给了回调函数之后，回调函数又是在主进程上执行的，那么就会出现打印结果是同步的效果。我们上面func2里面注销的时间模块打开看看
    #     p.apply_async(func1,args=(i,),callback=func2)

    p.apply_async(func1, args=(10,), callback=func2)
    p.close()
    p.join()
    # 返回值被当作回调函数的参数
    """
    func1
    func2
    100
    """

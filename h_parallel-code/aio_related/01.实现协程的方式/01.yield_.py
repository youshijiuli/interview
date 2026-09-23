#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.yield_.py
# @Author:Mysticat


import time

def func1():
    print(1)
    time.sleep(1)
    print(2)

def func2():
    print(3)
    time.sleep(1)
    print(4)


if __name__ == '__main__':
    func1()
    func2()



# 拓展

# def create_num(num):
#     a, b = 0, 1
#     current_num = 0
#     while current_num < num:
#         res = yield a       # 1.yield a  2.赋值
#         print(res)
#         a, b = b, a + b
#         current_num += 1
#
#     return 'i am amy'
#
# g = create_num(5)

# 1.第一次激活生成器 使用g.send(None)必须是发送的None
# print(g.send(None))
# print(g.send("hello"))

# 2.先用 next() 来激活生成器 再使用g.send()，此时就可以传入非None的参数
# print(next(g))
# print(g.send("world"))

# print(next(g))
# print(g.send("world"))

# g.close()   # 关闭生成器
# print(next(g))  # 报错：StopIteration

# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))

# 返回值再异常中
# while True:
#     try:
#         ret = next(g)
#         print(ret)
#     except Exception as e:
#         print("返回值：",e)
#         break
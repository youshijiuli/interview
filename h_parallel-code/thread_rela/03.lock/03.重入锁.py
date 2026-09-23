#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.重入锁.py
# @Author:Mysticat


# import time
# import threading
#
# num = 100
#
#
# def demo1(nums, mutex):
#     global num
#     # 加锁
#     mutex.acquire()
#     mutex.acquire()
#     for _ in range(nums):
#         num += 1
#     mutex.release()
#     mutex.release()
#     print(f'demo1 -- {num}')
#
#
# def demo2(nums, mutex):
#     global num
#     mutex.acquire()
#     for _ in range(nums):
#         num += 1
#     mutex.release()
#     print(f'demo2 -- {num}')
#
#
# def main():
#     # 创建互斥锁
#     # lock = threading.Lock()
#
#     # 重入锁
#     mutex = threading.RLock()
#     """
#     加锁 与 解锁 的 个数保持一致
#     """
#     t1 = threading.Thread(target=demo1, args=(1000000, mutex))
#     t2 = threading.Thread(target=demo2, args=(1000000, mutex))
#
#     t1.start()
#     t2.start()
#
#     time.sleep(1)
#     print(f'main thread -- {num}')
#
#
# if __name__ == '__main__':
#     main()
#     """
#     demo1 -- 1000100
#     demo2 -- 2000100
#     main thread -- 2000100
#     """




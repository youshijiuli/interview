#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :05.互斥锁.py
# @Author:Mysticat

import threading

g_num = 0


lock = threading.Lock()


def sum1():
    lock.acquire()
    for _ in range(1000000):
        global g_num
        g_num += 1

    print(g_num)

    lock.release()



# 每次只有一个线程可以获得锁，如果另一个线程试图获得锁，那个会变为“blocked”状态，即“阻塞”
# 知道拥有锁的线程使用release释放锁，锁进入“unlocked”状态，另一个线程才能获得锁



sum2 = sum1

print(sum1)
print(sum2)


if __name__ == '__main__':

    sum1_thread = threading.Thread(target=sum1)
    sum2_thread = threading.Thread(target=sum2)


    sum1_thread.start()
    sum2_thread.start()


    """
    <function sum1 at 0x10d1b39a0>
    <function sum1 at 0x10d1b39a0>
    1000000
    2000000
    """

    # 不加锁可能导致数据混乱




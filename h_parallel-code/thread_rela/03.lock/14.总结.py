#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :14.总结.py
# @Author:Mysticat


from threading import Thread, Lock, RLock
import time


# mutexA = Lock()
# mutexB = Lock()
mutexA = mutexB = RLock()
# 类只要加括号多次 产生的肯定是不同的对象
# 如果你想要实现多次加括号等到的是相同的对象 单例模式


class MyThead(Thread):
    def run(self):
        self.func1()
        self.func2()

    def func1(self):
        mutexA.acquire()
        print('%s 抢到A锁'% self.name)  # 获取当前线程名
        mutexB.acquire()
        print('%s 抢到B锁'% self.name)
        mutexB.release()
        mutexA.release()

    def func2(self):
        mutexB.acquire()
        print('%s 抢到B锁'% self.name)
        time.sleep(2)
        mutexA.acquire()
        print('%s 抢到A锁'% self.name)  # 获取当前线程名
        mutexA.release()
        mutexB.release()


if __name__ == '__main__':
    for i in range(10):
        t = MyThead()
        t.start()


# ================================================================

from threading import Thread,Lock
import time


mutex = Lock()
money = 100


def task():
    global money
    # with mutex:
    #     tmp = money
    #     time.sleep(0.1)
    #     money = tmp -1
    mutex.acquire()
    tmp = money
    time.sleep(0.1)  # 只要你进入IO了 GIL会自动释放
    money = tmp - 1
    mutex.release()


if __name__ == '__main__':
    t_list = []
    for i in range(100):
        t = Thread(target=task)
        t.start()
        t_list.append(t)
    for t in t_list:
        t.join()
    print(money)



"""
100个线程起起来之后  要先去抢GIL
我进入io GIL自动释放 但是我手上还有一个自己的互斥锁
其他线程虽然抢到了GIL但是抢不到互斥锁 
最终GIL还是回到你的手上 你去操作数据



"""

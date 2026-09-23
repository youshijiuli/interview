#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.死锁.py
# @Author:Mysticat


import threading
import time


class MyThread1(threading.Thread):
    def run(self):
        mutexA.acquire()
        # mutexA上锁后，延时1秒，等待另外那个线程 把mutexB上锁
        print(self.name + '----do1---up----')
        time.sleep(1)

        mutexB.acquire() # # 此时会堵塞，因为这个mutexB已经被另外的线程抢先上锁了
        # 程序就卡在这里，夯住了，因为被别人先上锁
        print(self.name + '----do1---down----')
        mutexB.release()

        mutexA.release()


class MyThread2(threading.Thread):
    def run(self):
        mutexB.acquire()
        # mutexA上锁后，延时1秒，等待另外那个线程 把mutexB上锁
        print(self.name + '----do1---up----')
        time.sleep(1)

        mutexA.acquire()
        print(self.name + '----do2---down----')
        mutexA.release()

        # 对mutexB解锁
        mutexB.release()









if __name__ == '__main__':
    mutexA = threading.Lock()
    mutexB = threading.Lock()
    t1 = MyThread1()
    t2 = MyThread2()

    t1.start()
    t2.start()
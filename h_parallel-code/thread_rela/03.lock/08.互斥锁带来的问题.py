#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :08.互斥锁带来的问题.py
# @Author:Mysticat


import time
import threading

mutexA = threading.Lock()
mutexB = threading.Lock()


class MyThread1(threading.Thread):
    def run(self):
        mutexA.acquire()
        print(self.name + '----do1---up----')
        time.sleep(1)
        mutexB.acquire()

        print(self.name + '----do1---down----')

        mutexB.release()

        mutexA.release()


class MyThread2(threading.Thread):
    def run(self):
        mutexB.acquire()
        print(self.name + '----do1---up----')
        time.sleep(1)
        mutexA.acquire()

        print(self.name + '----do1---down----')

        mutexA.release()

        mutexB.release()


if __name__ == '__main__':
    t1 = MyThread1()
    t2 = MyThread2()
    t1.start()
    t2.start()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test03.py
# @Author:Mysticat


# 死锁

import time
from threading import Thread, Lock

lock = Lock()


def eat(name):
    lock.acquire()
    print(name, '抢到面了')
    lock.acquire()
    print(name, '抢到叉子了')
    print(name, '吃面')
    time.sleep(0.1)
    lock.release()
    print(name, '放下叉子了')
    lock.release()
    print(name, '放下面了')


def eat2(name):
    lock.acquire()
    print(name, '抢到叉子了')
    lock.acquire()
    print(name, '抢到面了')
    print(name, '吃面')
    lock.release()
    print(name, '放下面了')
    lock.release()
    print(name, '放下叉子了')


Thread(target=eat, args=('alex',)).start()
Thread(target=eat2, args=('wusir',)).start()
Thread(target=eat, args=('taibai',)).start()
Thread(target=eat2, args=('大壮',)).start()

import time
from threading import Thread, Lock, RLock

fork_lock = noodle_lock = RLock()


# fork_lock = RLock()

def eat(name):
    noodle_lock.acquire()
    print(name, '抢到面了')
    fork_lock.acquire()
    print(name, '抢到叉子了')
    print(name, '吃面')
    time.sleep(0.1)
    fork_lock.release()
    print(name, '放下叉子了')
    noodle_lock.release()
    print(name, '放下面了')


def eat2(name):
    fork_lock.acquire()
    print(name, '抢到叉子了')
    noodle_lock.acquire()
    print(name, '抢到面了')
    print(name, '吃面')
    noodle_lock.release()
    print(name, '放下面了')
    fork_lock.release()
    print(name, '放下叉子了')


Thread(target=eat, args=('alex',)).start()
Thread(target=eat2, args=('wusir',)).start()
Thread(target=eat, args=('taibai',)).start()
Thread(target=eat2, args=('大壮',)).start()

# 死锁现象：多把锁，交替使用，在第一把锁没有释放前就获取到了第二把锁，是指两个或两个以上的进程或线程在执行过程中，因争夺资源而造成的一种互相等待的现象，若无外力作用，它们都将无法推进下去。此时称系统处于死锁状态或系统产生了死锁，这些永远在互相等待的进程称为死锁进程。
# 解决办法 ：把所有的互斥锁改成一把递归锁，但是这样影响效率，以后可慢慢理清头绪，再改成一把锁
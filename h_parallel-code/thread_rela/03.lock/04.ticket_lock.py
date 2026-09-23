#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :04.ticket_lock.py
# @Author:Mysticat


import time
import threading

g_ticket = 100
i = 0

lock = threading.Lock()


def sold(n):
    global g_ticket, i
    while True:
        lock.acquire()
        if g_ticket:
            i += 1
            g_ticket -= 1
            time.sleep(1)
            print('线程%d第%d张，剩%d张' % (n, i, g_ticket))
            lock.release()
        else:
            lock.release()
            break


for index in range(6):
    sold_thread = threading.Thread(target=sold, args=(index + 1,))
    sold_thread.start()

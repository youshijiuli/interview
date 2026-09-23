#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import json
from multiprocessing import Process,Lock
def buy_ticket(user,lock):
    with lock:
        time.sleep(0.02)
        with open('ticket_count') as f:
            dic=json.load(f)
        if dic['count']>0:
            print('%s买到了'%(user))
            dic['count']-=1
        else:
            print('%s没买到票票'%(user))

        time.sleep(0.02)
        with open('ticket_count', 'w') as f:
            json.dump(dic,f)


if __name__ == '__main__':
    lock=Lock()
    for i in range(10):
        p=Process(target=buy_ticket,args=('user%s'%i,lock))
        p.start()
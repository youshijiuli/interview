#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.yield_from.py
# @Author:Mysticat

import time
from multiprocessing import Process,Queue

class MyProcess(Process):

    def __init__(self,name,mq):
        super().__init__()
        self.name = name
        self.mq = mq
    def run(self):
        print(f"Process:{self.name} start")
        print(f"get Data:{self.mq.get()}")
        time.sleep(2)
        self.mq.put(self.name)
        print(f"Process:{self.name} end")




if __name__ == '__main__':
    p_list = []
    mq = Queue()
    mq.put("1")
    mq.put("2")
    mq.put("3")

    for i in range(3):
        p = MyProcess("p{}".format(i),mq)
        p.start()
        p_list.append(p)

    for t in p_list:
        t.join()


    print(mq.get())
    print(mq.get())
    print(mq.get())


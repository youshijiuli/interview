#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.queue_.py
# @Author:Mysticat

import time
from multiprocessing import Process, Queue


class MyProcess(Process):
    def __init__(self, name, mq):
        super().__init__()
        self.name = name
        self.mq = mq

    def run(self):
        print(f'Process:{self.name} is running')
        print(f'get Data:{self.mq.get()}')
        time.sleep(2)
        self.mq.put(f'new data:{self.name}')
        print(f'Process:{self.name} ending...')


if __name__ == '__main__':
    queue = Queue()
    queue.put('1')
    queue.put('2')
    queue.put('3')

    p_list = []

    for i in range(3):
        p = MyProcess(f'p{i + 1}', queue)
        p_list.append(p)

    for p in p_list: p.start()
    for p in p_list: p.join()

    print(queue.get())
    print(queue.get())
    print(queue.get())

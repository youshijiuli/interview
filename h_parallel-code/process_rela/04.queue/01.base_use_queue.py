#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :01.base_use_queue.py
# @Author:Mysticat


import time
import random
from multiprocessing import Process, Queue, set_start_method


class Producer(Process):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        for _ in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            print("Process Producer : item %d appended to queue %s" % (item, self.name))
            # time.sleep(1)
            # print("The size of queue is %s" % self.queue.qsize())


class Consumer(Process):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                print('the queue is empty')
                break # 退出死循环

            else:
                time.sleep(1)
                item = self.queue.get()
                print('Process Consumer : item %d popped from by %s \n' % (item, self.name))
                time.sleep(1)


if __name__ == '__main__':
    set_start_method('fork')
    queue = Queue()
    process_producer = Producer(queue)
    process_consumer = Consumer(queue)
    process_producer.start()
    process_consumer.start()

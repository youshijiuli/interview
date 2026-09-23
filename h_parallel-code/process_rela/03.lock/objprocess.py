#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
from multiprocessing import Process


class MyProcess1(Process):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        super().__init__()

    def run(self):
        print(self.x, self.y, os.getpid())
        for i in range(5):
            print('in process1 cls')
            time.sleep(1)


if __name__ == '__main__':
    mp = MyProcess1(1, 2)
    mp.daemon = True
    mp.start()
    print(mp.is_alive())
    # time.sleep(10)
    # mp.terminate()

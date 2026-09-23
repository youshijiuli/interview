#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.生产消费.py
# @Author:Mysticat


from multiprocessing import Process, Pipe


def consumer(p, name):
    left, right = p
    left.close()
    while True:
        try:
            baozi = right.recv()
            print(f'{name}收到包子：{baozi}')
        except EOFError:
            right.close()
            break


def producer(seq, p):
    left, right = p
    right.close()
    for i in seq:
        left.send(i)
    left.close()


if __name__ == '__main__':
    left, right = Pipe()
    c1 = Process(target=consumer, args=((left, right), 'c1'))
    c1.start()

    seq = (i for i in range(10))
    producer(seq, (left, right))

    right.close()
    left.close()

    c1.join()
    print('主进程')

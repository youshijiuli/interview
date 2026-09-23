#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :02.进阶.py
# @Author:Mysticat

import multiprocessing


def create_image(pipe):
    output, _ = pipe
    for item in range(10):
        output.send(item)
    output.close()


def multiply_items(pipe1, pipe2):
    close, input = pipe1
    close.close()
    output, _ = pipe2

    try:
        while True:
            item = input.recv()
            output.send(item ** 2)
    except EOFError:
        output.close()


if __name__ == '__main__':
    # 第一个进程管道发出数字
    p1 = multiprocessing.Pipe(True)
    process1 = multiprocessing.Process(
        target=create_image, args=(p1,)
    )
    process1.start()

    # 第二个管道接受数字并计算
    p2 = multiprocessing.Pipe(True)
    process2 = multiprocessing.Process(
        target=multiply_items,args=(p1,p2)
    )
    process2.start()

    p1[0].close()
    p2[0].close()

    try:
        while True:
            print(p2[1].recv())
    except EOFError:
        print("End")

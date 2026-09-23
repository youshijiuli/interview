#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :index01.py
# @Author:Mysticat


from multiprocessing import Process, Pipe


def func(conn):
    """向主进程发送消息"""
    conn.send([42, None, 'hello'])
    conn.close()


if __name__ == '__main__':
    # #管道的接收端和发送端
    parent_conn, child_conn = Pipe()
    # 把发送端传进子进程要执行的函数中
    process = Process(
        target=func, args=(child_conn,)
    )

    process.start()
    print(parent_conn.recv()) # [42, None, 'hello']
    process.join()

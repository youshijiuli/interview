#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :11.互斥锁3.py
# @Author:Mysticat


import time
from threading import Thread, Lock


class Account:
    def __init__(self, money, name):
        self.money = money
        self.name = name


class Drawing(Thread):

    def __init__(self, account, drawingNum):
        super().__init__()
        self.account = account
        self.drawingNum = drawingNum
        self.expenseTotal = 0

    def run(self):
        lock1.acquire()
        if self.account.money < self.drawingNum:
            print("账户余额不足！")
            lock1.release()
            return


        self.account.money -= self.drawingNum
        self.expenseTotal = self.drawingNum

        lock1.release()
        print(f'一共消费{self.expenseTotal},剩余{self.account.money}')


if __name__ == '__main__':
    a1 = Account(100, 'lsia')
    lock1 = Lock()

    draw1 = Drawing(a1, 80)
    draw2 = Drawing(a1, 80)

    draw1.start()
    draw2.start()

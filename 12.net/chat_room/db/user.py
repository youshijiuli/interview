#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :user.py
# @Author:Mysticat


import sqlite3


class User:
    # TODO:给名字长度限制
    def __init__(self, name=None, password=None):
        self.name = name
        if len(password) < 6:
            raise ValueError('密码长度过短')
        self.password = password


class Repository:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def select_others(self, names):
        sql = 'select name from main.user from where id in (%s);' % ','.join('?' * len(names))
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def insert_user(self, user):

        try:
            sql = "INSERT INTO main.user(name, password) VALUES (?, ?)"
            self.cursor.execute(sql, (user.name, user.password))
            row_id = self.cursor.lastrowid
        except sqlite3.IntegrityError:
            self.conn.rollback()
            raise ValueError("用户名已存在")
        self.conn.commit()
        self.cursor.close()
        return row_id

    def search_user(self, name):
        sql = 'select name,password from main.user where name=(?);'
        self.cursor.execute(sql, (name,))
        row = self.cursor.fetchone()
        self.cursor.close()
        return row

    def login(self, user: User):
        row = self.search_user(user.name)
        if user.password != row[1]:
            raise ValueError('密码错误')
        print(row)
        return

    def register(self, user: User):
        latest_id = self.insert_user(user)
        print(latest_id)
        return latest_id

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    repo = Repository('data.sqlite3')
    testUser = User('lisa', '12345678')
    repo.register(testUser)
    print('注册成功！！！')

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :init_db.py
# @Author:Mysticat


import sqlite3


conn = sqlite3.connect('data.sqlite3')
sql = """
create table user(
id integer not null primary key AUTOINCREMENT,
name varchar(32) not null ,
password varchar(32) not null 
);
"""


cursor = conn.cursor()

cursor.execute(sql)

conn.commit()

print('表创建成功！！！')

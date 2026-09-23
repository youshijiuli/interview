#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :his.py
# @Author:Mysticat


import multiprocessing
import os

"""
文件拷贝
"""


def copy_file(file_name, new_fold_name, old_fold_name):
    # 读取file_name文件内容
    with open(old_fold_name + "/" + file_name, "rb") as f:
        content = f.read()

    # 保存到新的文件夹中
    with open(new_fold_name + "/" + file_name, "wb") as n_f:
        n_f.write(content)


def main():
    # 1.获取用户要复制的文件夹名称
    old_fold_name = input("请输入要复制的文件夹名字")

    # 2.创建新的文件夹
    new_fold_name = old_fold_name + "附件"

    # 3.判断该文件路径是否存在 不存在才 创建文件夹
    if not os.path.exists(new_fold_name):
        os.mkdir(new_fold_name)

    # 4.获取老的文件夹 下 所有需要被拷贝文件的 名字
    file_names = os.listdir(old_fold_name)
    # print(file_names)

    # 同步 拷贝
    # 5.创建进程池
    po = multiprocessing.Pool(5)

    # 6.添加拷贝任务
    for file_name in file_names:
        po.apply_async(copy_file, args=(file_name, new_fold_name, old_fold_name))

    po.close()
    po.join()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :v1.py
# @Author:Mysticat


import multiprocessing

import os

import shutil


def copy_dir(src_file_path, tar_file_path, file_name):
    with open(tar_file_path, 'w') as t_file:
        # src_file = src_dir + "\\" + file_name  # 源文件路径
        with open(src_file_path, 'r') as file:
            # 读源文件,写到目标文件
            # 4.死循环读取当前文件的内容
            while True:
                data = file.read(1024)  # 每次读1024个字符 因为默认 r 模式 读的是字符
                if data:
                    # 有内容:写
                    t_file.write(data)

                else:
                    print("%s拷贝完成" % file_name)
                    # print(a)  # 因为子进程报错了
                    # print("拷贝完成")
                    break


if __name__ == '__main__':

    src_dir = r'.\\test'
    tar_dir = 'C:\\Users\\LS\\Desktop' + '\\' + src_dir
    # print(os.path.isdir(tar_dir))
    # 判断目标文件夹是否存在
    if os.path.exists(tar_dir):
        # 文件夹存在则删除
        shutil.rmtree(tar_dir)

    # 重新创建目标文件夹
    os.mkdir(tar_dir)

    # 获取文件夹内文件
    file_name_list = os.listdir(src_dir)

    # 创建进程池
    pool = multiprocessing.Pool()

    for file_name in file_name_list:
        print(file_name)
        # 获取原文件夹中文件路径
        src_file_path = src_dir + '\\' + file_name
        # 目标文件夹路径
        tar_file_path = tar_dir + '\\' + file_name
        # 异步拷贝
        pool.apply_async(copy_dir, args=(src_file_path, tar_file_path, file_name))

    pool.close()
    pool.join()







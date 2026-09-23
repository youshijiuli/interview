#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :index.py
# @Author:Mysticat


"""


# 完成将一个文件夹和文件复制到另一个文件夹中

通过多进程实现文件的拷贝

v1:拷贝文件，不拷贝文件夹

"""

# 用户输入文件路径，
# 遍历此文件路径下的所有文件
# 将每一个文件拷贝至我们指定的另外一个文件夹


import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor


def copy_file(filename: str, old_folder: str, new_folder: str):
    """
    文件拷贝,先读再去写
    :param filenam:
    :param old_folder:
    :param new_folder:
    :return:
    """
    with open(f'{old_folder}/{filename}', 'r') as f1:
        content = f1.read()

    with open(f'{new_folder}/{filename}', 'w') as f2:
        f2.write(content)


def main():
    # 1.获取要复制的文件夹名称
    old_folder = input('请输入文件夹路径:').strip()

    # 2.构造新的文件夹
    new_filder = './file_copy'

    # 3. 文件夹不存在就创建
    if not os.path.exists(new_filder):
        os.makedirs(new_filder)

    # 4.遍历文件夹下所遇的文件
    file_list = os.listdir(old_folder)

    # 5.创建进程池
    # pool = multiprocessing.Pool(5)
    pool = ProcessPoolExecutor(5)

    # 6.添加文件拷贝任务
    for filename in file_list:
        pool.submit(copy_file, filename, old_folder, new_filder)



if __name__ == '__main__':
    main()

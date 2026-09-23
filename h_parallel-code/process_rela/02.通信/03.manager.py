#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :03.manager.py
# @Author:Mysticat


from multiprocessing import Process, Manager


def func(name, m_list: list, m_dic):
    m_dic[name] = 'lisa'
    m_list.append('hello')


if __name__ == '__main__':
    with Manager() as mgr:
        m_list = mgr.list()
        m_dic = mgr.dict()

        m_list.append('world')
        # 两个进程不能直接互相使用对象，需要互相传递
        p1 = Process(target=func, args=('p1', m_list, m_dic))
        p1.start()
        p1.join()

        print(f'主进程：{m_list}')
        print(f'主进程：{m_dic}')

    """
    主进程：['world', 'hello']
    主进程：{'p1': 'lisa'}
    """
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :scheduler.py
# @Author:Mysticat


# 调度器
from modules.downloader import Downloader
from modules.hasher import Hasher
from modules.storager import Storage
import utils
import os
from const import CalcType

# 使数据打印格式更好看,转换成报表
import prettytable


class Scheduler():
    """ 调度模块 """

    def __init__(self):
        # 初始化调度模块
        self.downloader = Downloader()
        self.hasher = Hasher()
        self.storager = Storage()

    def _wrap_path(self, md5):
        """ 将MD5字符串,改造成存储路径 """
        filename = '%s.jpg' % md5
        STORAGE_PATH = os.path.join('.', 'images')
        path = os.path.join(STORAGE_PATH, filename)
        return path

    def set_calc_type(self, type_):
        """ 设置类型 """
        self.downloader.set_calc_type(type_)
        self.hasher.set_calc_type(type_)
        self.storager.set_calc_type(type_)

    def statictics(self, *args):
        """ 漂亮的表格式的输出这些数据 """
        table = prettytable.PrettyTable(['类型', '单线程总耗时', '多线程总耗时', '多进程总耗时', '多线程提升率'])

        network_row = ['network']
        cpu_row = ['cpu']
        disk_row = ['disk']
        for i in range(len(args) + 1):
            if i == 3:
                print(network_row[1])
                print(network_row[2])
                network_row.append((network_row[1] - network_row[2]) / network_row[1] * 100)
                cpu_row.append((cpu_row[1] - cpu_row[2]) / cpu_row[1] * 100)
                disk_row.append((disk_row[1] - disk_row[2]) / disk_row[1] * 100)
                break
            log = args[i]
            # 单线程的数据,第二次遍历多线程的数据
            network_row.append(log['network_time'][0])
            cpu_row.append(log['cpu_time'][0])
            disk_row.append(log['disk_time'][0])

        table.add_row(network_row)
        table.add_row(cpu_row)
        table.add_row(disk_row)
        print(table)

    def process(self):
        time_statictics = {}
        time_statictics['network_time'] = []  # 网络下载用时
        time_statictics['cpu_time'] = []  # 计算密集型,hash
        time_statictics['disk_time'] = []  # 存盘和网络下载都是io
        # 引入计时器,计算运行时间
        timer = utils.Timer()

        # 1.加载图片
        url_list = utils.urllist()

        # 2. 调度下载模块
        timer.tick()
        content_list = self.downloader.process(url_list)
        time_cost = timer.tock()
        time_statictics['network_time'].append(time_cost)

        # 3. 调度hash模块
        timer.tick()
        md5_list = self.hasher.process(content_list)
        for md5 in md5_list:
            print(md5)
        time_cost = timer.tock()
        time_statictics['cpu_time'].append(time_cost)

        # 4. 存储模块的调度
        # 使用zip函数将 MD5的内容与 url_list 组合, 其中调用函数,将MD5转化为路径
        timer.tick()
        item_list = [(content, self._wrap_path(md5)) for content, md5 in zip(content_list, md5_list)]
        self.storager.process(item_list)
        time_cost = timer.tock()
        time_statictics['disk_time'].append(time_cost)
        return time_statictics


if __name__ == '__main__':
    scheduler = Scheduler()
    # 单线程运行
    s_time_statictics = scheduler.process()
    # scheduler.statictics(time_statictics)
    # 多线程运行
    scheduler.set_calc_type(CalcType.MultiThread)
    m_time_statictics = scheduler.process()
    # 多进程的运行
    scheduler.set_calc_type(CalcType.MultiProcess)
    p_time_statictics = scheduler.process()
    # 合并数据统一分析
    scheduler.statictics(s_time_statictics, m_time_statictics, p_time_statictics)

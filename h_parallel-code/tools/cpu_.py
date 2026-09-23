#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :cpu_.py
# @Author:Mysticat

import psutil
import time
import os


def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(1)
    return cpu_usage


def get_memory_usage():
    memory_usage = psutil.virtual_memory().percent
    return memory_usage


def get_disk_usage():
    disk_usage = psutil.disk_usage('/').percent
    return disk_usage


def get_network_usage():
    network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    return network_usage


def get_system_uptime():
    uptime = time.time() - psutil.boot_time()
    return uptime


def get_system_temperature():
    psutil.sensors_temperatures()
    return psutil.sensors_temperatures()


def get_system_load():
    # load = psutil.getloadavg()
    return psutil.getloadavg()


def get_system_info():
    return psutil.virtual_memory().total


def get_system_cpu_count():
    return psutil.cpu_count()


def get_system_cpu_freq():
    return psutil.cpu_freq()


def get_system_cpu_percent():
    return psutil.cpu_percent(interval=1)


def get_system_cpu_times():
    return psutil.cpu_times()


def get_system_cpu_times_percent():
    return psutil.cpu_times_percent(interval=1)


def get_system_cpu_stats():
    return psutil.cpu_stats()


if __name__ == "__main__":
    print(get_cpu_usage())

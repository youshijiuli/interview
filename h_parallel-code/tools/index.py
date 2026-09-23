#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :index.py
# @Author:Mysticat


import psutil
from functools import reduce


# arr = [1, 2, 3, 4, 5]

# sum = reduce(lambda accumulator, currentValue: accumulator + currentValue, arr)
# print(sum)  # 输出：15

def get_all_processes():
    processes = []
    for process in psutil.process_iter():
        try:
            processes.append(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes


process_dict = {}


def main():
    processes = get_all_processes()
    print(f"=============={len(processes)}=========================")
    for process in processes:
        # #    print(f"Process: {process}")
        #    print(process.name())
        if process_dict.get(process.name()) is not None:
            process_dict[process.name()] += 1
        else:
            process_dict[process.name()] = 1

    for key, value in process_dict.items():
        print(f"{key} : {value}")

    res_count = reduce(lambda accumulator, currentValue: accumulator + currentValue, process_dict.values())
    print(len(processes) == res_count)


if __name__ == "__main__":
    main()

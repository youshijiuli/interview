#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :start.py
# @Author:Mysticat


import os,sys

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(
            __file__
        )
    )
)

# print(BASE_DIR)

sys.path.append(BASE_DIR)





if __name__ == '__main__':
    from lib import management
    argv_parser = management.ManagementTool(sys.argv)
    # argv_parser.execute()
    argv_parser.start()

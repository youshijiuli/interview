#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test03.py
# @Author:Mysticat


import time
import uuid
from concurrent.futures import ThreadPoolExecutor


def task(args):
    time.sleep(1)
    print(f'execute task -- {args}')
    return {
        "id": str(uuid.uuid4()),
        'data': {'name': 'lisa'}
    }


pool = ThreadPoolExecutor(10)
result = pool.map(task, range(20))

print(result)
print(type(result))

pool.shutdown()

for item in result:
    print(item)

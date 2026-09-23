#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :06.flask_process_pool.py
# @Author:Mysticat

import math
import json

from flask import Flask
from concurrent.futures import ProcessPoolExecutor

app = Flask(__name__)


def is_prime(n: int):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True


@app.route("/is_prime/<numbers>")
def api_is_prime(numbers):
    number_list = [
        list(x) for x in numbers.split(',')
    ]
    result = pool.map(is_prime, number_list)
    return json.dumps(
        dict(zip(number_list, result))
    )


if __name__ == '__main__':
    pool = ProcessPoolExecutor(10)
    app.run()

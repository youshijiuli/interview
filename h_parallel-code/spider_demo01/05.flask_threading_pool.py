#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :05.flask_threading_pool.py
# @Author:Mysticat

import json
import time
from flask import Flask
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

pool = ThreadPoolExecutor(10)


def read_fiel():
    time.sleep(.1)
    return 'result'


def read_api():
    time.sleep(0.2)

    return 'api result'


def read_db():
    time.sleep(.3)
    return 'db result'


@app.route('/')
def index():
    result_file = pool.submit(read_fiel)
    result_api = pool.submit(read_api)
    result_db = pool.submit(read_db)

    result = json.dumps(
        {
            "result_file": result_file.result(),
            "result_api": result_api.result(),
            "result_db": result_db.result(),
        }
    )

    return result


if __name__ == '__main__':
    app.run()

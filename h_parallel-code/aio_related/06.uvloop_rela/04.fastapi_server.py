#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :04.fastapi_server.py
# @Author:Mysticat


import uvicorn
import asyncio
import aioredis
from fastapi import FastAPI

app = FastAPI()

# 创建redis连接池
REDIS_POOL = aioredis.ConnectionsPool('redis://localhost:6379', password=None, minsize=1, maxsize=10)


@app.get('/')
def index():
    # 普通视图函数
    return {'message': 'hello world'}


@app.get('/red')
async def red():
    # 异步视图
    print('请求来了...')
    await asyncio.sleep(3)

    # 获取连接池中的一个链接
    conn = await REDIS_POOL.acquire()
    redis = aioredis.Redis(conn)

    # 设置值
    await redis.hmset_dict('car_fastApi', key1=1, key2=2, key3=3)

    # 读取值
    result = await redis.hgetall('car_fastApi', encoding='utf-8')
    print(result)

    # 将单个连接归还给连接池
    REDIS_POOL.release(conn)

    return result


if __name__ == '__main__':
    # FastAPI_server为当前这个脚本文件的名称
    uvicorn.run("FastAPI_server:app", host='127.0.0.1', port=5000, log_level='info')

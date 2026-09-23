#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server.py
# @Author:Mysticat


import asyncio


async def handle_echo(reader,writer):
    """客户端连接后回调的协程函数，负责对接收到的内容进行处理；start_server函数内部创建的reader和writer对象会传进该函数，从而transport和protocol得到统合"""
    data = await reader.read(100) #等待并尝试从接收缓冲区读取100个字节
    message = data.decode('utf-8')
    addr = writer.get_extra_info('peername') #获取连接套接字的远端地址


    print(f'received {message!r} from {addr!r}')


    print(f'send:{message!r}')

    writer.write(data) # 将data写入缓冲区
    await writer.drain() #控制write()方法写入的流量

    print('close the connection')

    writer.close() #关闭writer对象底层的连接套接字
    # 该方法Should be called after close() to wait until the underlying connection is closed.
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_echo,'127.0.0.1',9000
    )
    addr = server.sockets[0].getsockname()
    print(f'serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
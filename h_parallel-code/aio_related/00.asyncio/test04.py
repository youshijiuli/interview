#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test04.py
# @Author:Mysticat

#
# import asyncio
#
# async def cancel_me():
#     print('cancel_me(): before sleep')
#
#     try:
#         await asyncio.sleep(3600)
#     except asyncio.CancelledError:
#         print('cancel_me():cancel sleep')
#         raise
#     finally:
#         print('cancel_me():after sleep')
#
#
# async def main():
#     # 从创建cancel_me()的task开始，事件循环中就同时存在main()和cancel_me()这2个task了
#     task = asyncio.create_task(cancel_me())
#     # main()协程中断1秒，控制权移交给cancel_me()协程
#     await asyncio.sleep(1)
#
#     # 等待1s之后，就取消task
#     task.cancel()
#
#     try:
#         # 等待task，此时控制权又一次移交给cancel_me()协程，然后【取消错误】异常才会在该协程中冒泡
#         await task
#     except asyncio.CancelledError:
#         # cancel_me()内部的【取消错误】异常向上冒泡，然后被main()此处的代码捕获
#         print('main(): cancel_me is cancelled now')
#
# asyncio.run(main())



import asyncio

async def cancel_me():
    print('cancel me started...')
    await asyncio.sleep(3600)


async def main():
    # 从创建cancel_me()的task开始，事件循环中就同时存在main()和cancel_me()这2个task了
    task = asyncio.create_task(cancel_me())
    # main()协程中断1秒，控制权移交给cancel_me()协程
    await asyncio.sleep(1)
    task.cancel() # 等待1s之后，取消task

    try:
        await task #等待task，此时控制权又一次移交给cancel_me()协程，然后【取消错误】异常才会在该协程中冒泡
    # 这里忽略掉冒到main()协程中的异常，才能继续执行后面状态检查
    except asyncio.CancelledError:
        pass

    print('cancle me is cnacelled?',task.cancelled())


asyncio.run(main())
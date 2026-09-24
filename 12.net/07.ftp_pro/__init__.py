#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :__init__.py
# @Author:Mysticat


# 【1】 分为服务端和客户端，要求可以有多个客户端同时操作。
#
# 【2】 客户端可以查看服务器文件库中有什么文件。
#
# 【3】 客户端可以从文件库中下载文件到本地。
#
# 【4】 客户端可以上传一个本地文件到文件库。
#
# 【5】 使用print在客户端打印命令输入提示，引导操作

# 1.验证客户端合法性(了解)
    # 登录 : 只要有个性化设计的时候就需要登录
    # 登录和合法性验证二选一,如果做登录功能就不需要做合法性验证了
# 2.并发的socketserver(重点)
# 3.分析ftp作业的需求
    # https://www.cnblogs.com/Eva-J/articles/7642557.html

# 实现进度条功能
import sys
def processBar(num, total):
    rate = num / total
    rate_num = int(rate * 100)
    if rate_num == 100:
        r = '\r%s>%d%%\n' % ('=' * rate_num, rate_num,)
    else:
        r = '\r%s>%d%%' % ('=' * rate_num, rate_num,)
    print(r,flush=True)

processBar(2048,10240)

# 用户登陆，加密认证
    #加密的过程至少在server端进行一次

# 用户注册

# 管理用户登录 注册成功之后才能进行上传\下载

# 多用户同时登陆 -- socketserver实现

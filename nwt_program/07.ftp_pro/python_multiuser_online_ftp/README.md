# Python多用户在线FTP

#### 项目介绍
简单的ftp程序

一，项目要求：


    1.用户加密认证
    
    2.允许同时多用户登录
    
    3.每个用户有自己的家目录 ，且只能访问自己的家目录
    
    4.对用户进行磁盘配额，每个用户的可用空间不同
    
    5.允许用户在ftp server上随意切换目录
    
    6.允许用户查看当前目录下文件
    
    7.允许上传和下载文件，保证文件一致性(md5)
    
    8.文件传输过程中显示进度条
    
    9.附加功能：支持文件的断点续传


二, 程序结构


    │  FTP_homework
    │  __init__.py
    │ 
    ├─client                # 客户端程序入口
    │  │  __init__.py
    │  ├─bin                # 可执行程序入口目录
    │  │      run.py
    │  │      __init__.py
    │  ├─config             # 配置文件目录
    │  │  │  settings.py    # 配置文件
    │  │  │  __init__.py      
    │  ├─core               # 主要逻辑程序目录
    │  │  │  ftp_client.py  # client端主程序模块
    │  │  │  __init__.py      
    │  ├─download           # 下载内容模块
    │  │      bg.jpg
    │  └─upload             # 上传内容模块
    │
    └─server                 # 服务端程序入口
    ├─bin
    │      run.py        # 可执行程序入口目录
    │      __init__.py
    ├─config             # 配置文件目录
    │  │  accounts.ini   # 账号密码配置文件
    │  │  settings.py    # 配置文件
    │  │  __init__.py       
    ├─core               # 主要逻辑程序目录
    │  │  ftp_server.py  # server端主程序模块
    │  │  main.py        # 主程序模块
    │  │  user_handle.py # 用户注册登录模块 
    └─home               # 家目录
        │  __init__.py
        ├─123            # 123用户的家目录
        │  └─bg.jpg
        └─111           # 111用户的家目录
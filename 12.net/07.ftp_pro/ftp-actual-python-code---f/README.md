# FTP实战python代码

#### 介绍
本项目基于python语言的socket通信编程，构建了FTP文件传输协议的客户端和服务端代码，模拟了两种数据传输模式，拥有较多的FTP原生命令功能，不过还缺少不同用户身份登录使用不同功能、使用命令对文件权限的判断这两项功能。

#### 软件架构
- 客户端、服务端之间使用socket创建TCP连接。
- 客户端打开程序首次进入FTP功能，需要先连接到服务端，此时会创建一个控制连接，连接成功后，客户端发送的命令都会通过控制连接发送给服务端，服务端执行命令
- 客户端与服务端之间需要传输数据时，比如客户端发送`ls`命令查看服务器上的文件，服务端会返回给客户端文件列表，或者客户端上传文件到服务端，需要传输数据，此时通过读取配置文件，选择使用被动或者主动模式，在客户端与服务端之间创建一个数据连接，数据就通过该连接进行传输。

#### 配置文件说明

- server_ftp_conf.txt： FTP服务端的配置文件
- client_ftp_conf.txt：FTP客户端的配置文件
- help.txt：支持的FTP命令说明
- user.db：存放用户信息


#### 使用说明

1.  主要查看查看`server_ftp_conf.txt`服务端配置文件：
  - `local_dir`、`user_db`参数需要调整
2.  客户端、服务端程序启动先后顺序任意，无影响

#### 支持的FTP命令

可以查看`help.txt`文件

- cd		
- pwd		
- put		
- get		
- ls		
- dir		
- mls		
- mdir		
- delete		
- quit		
- open		
- lcd		
- close		
- help


#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)

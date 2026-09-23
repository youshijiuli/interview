作业名称：选课系统
测试环境：win7系统，python3.7.0，工具:pycharm-community-2018.1.4
作者：肖蕾

作业题目: 开发一个支持多用户在线的FTP程序

要求：
1.用户加密认证                                  # 加密认证，引入cinfigparser 设置account_info.ini 相当于数据库 里面存 用户名和  密码的md5值
2.允许同时多用户登录                             # 并发编程知识这个功能没有实现
3.每个用户有自己的家目录 ，且只能访问自己的家目录   # 每个用户名一个单独的总文件，执行命令时到自己所在目录  os.chdir(self.homedir_conn[conn]['current_dir'])
4.对用户进行磁盘配额，每个用户的可用空间不同        # 可以在account_info.ini 文件自己设置 quota
5.允许用户在ftp server上随意切换目录              # cd
6.允许用户查看当前目录下文件                      # ls
7.允许上传和下载文件，保证文件一致性(md5)          # 客户端下载后为文件（md5）与服务器端 相同文件的（md5）值对比
8.文件传输过程中显示进度条                        # sys.stdout.write('\r'+str*int(round(float_rate * 10))+'[{0}%]'.format(rate))  time.sleep(0.05)
9.附加功能：支持文件的断点续传                     # 若所需下载的文件已在客户端存在，比较客户端client_file_size 与服务器文件 server_file_size 对比

题目:基于线程开发一个FTP服务器:
要求:
1.在之前开发的FTP基础上，开发支持多并发的功能
2.不能使用SocketServer模块，必须自己实现多线程
3.必须用到队列Queue模块，实现线程池
4.允许配置最大并发数，比如允许只有10个并发用户

# -----------------说明------------------------
1、用户名|密码 手动在 db/account_inf 中 建成：账户：alex，密码123；账户：egon 密码：123； 账户：victor,密码：123
2、启动服务端
3、再启动客户端
4、在原有的基础上实现服务端并发功能
    4.1.引入 queue实现线程池和最大并发数，设置最大并发数为2(q = queue.Queue(2))
    4.2.引入Thread模块实现并发
    4.3.增加链接循环和通信循环，增加客户端异常断开的try:except处理。

5、服务端已有文件：
    alex
        test
            3.jpg
        1.jpg
        2.jpg
    egon
         test
            3.jpg
        1.jpg
        2.jpg
        a.txt
    victor

客户端：
      upload：
            python.txt

6、ls 查询操作 def ls(self)： win7系统  print(recv_bytes.decode('gbk'))

7、交互指令： 例如  下载 get 1.jpg
                  上传 put  2.jpg
                  查看当前目录 ls
                  切换目录 cd test
                  新建目录 mkdir test
                  删除文件 rmdir





# 第十五章 Linux

> 来源：Python阶段面试题v2.md

1. 下面的linux命令中, 那个不能显示出文件的内容

   ```
   A.  tac
   B.  more
   C.  head
   D.  man
   ```

2. 默认情况下管理员创建了一个用户, 就会在()目录下创建一个用户主目录

   ```
   A.  /usr
   B.  /home
   C.  /root
   D.  /etc
   ```

3. 你使用命令"vi /etc/inittab"查看该文件的内容, 你不小心改动了一些内容, 为了防止系统出问题, 你不想保存所修改的内容, 你应该如何操作

   ```
   A.  在末行模式下, 键入:q!
   B.  在末行模式下, 键入:x!
   C.  在末行模式下, 键入:wq
   D.  在末行模式下, 键入"ESC"键直接退出vi
   ```

4. 用"rm -i", 系统会提示什么来让你确认

   ```
   A.  命令行的每个选择
   B.  是否真的删除
   C.  是否有写的权限
   D.  文件的位置
   ```

5. 在CentOS7.2中, 用一句话将所有的test.py进程全部杀死

6. 在CentOS7.2中, 如何查看程序执行所消耗的CPU, 内存等硬件资源

7. 写一个Bash Shell脚本来得到当前的日期,时间, 用户名和当前的工作目录

8. 如何查看当前登录用户

9. 如何定位占用端口8080的服务

10. 如何切换用户

11. 查找/tmp/path下的以A开头的文件

12. 如有两台机器a/b, a的ip地址包括45.32.12.222, 10.10.121.22 b的ip地址包括45.32.12.226,10.10.121.69,两台机器的ssh监听端口为11111

    ```
    请写出远程登录机器a的命令
    
    请写出从a远程登录b的命令
    
    请说明从b机器访问qq.com时的详细过程, 以及到qq.com记录到的ip
    ```

13. 计划任务---如何让abc.sh每周一执行一次 若执行失败的原因是什么

14. 如何查看发往本机8080端口的流量

15. 现有一文件文件内容为ip地址及路径, 例如192.168.31.9 /tmp/destpath, 现需要将本机的hello.txt文件发送到文件记录的机器相应的目录中, 编程实现(shell)

16. 在linux中, 如何批量的删除多个Python进程

17. 下面那个函数能够在linux下创建一个子进程

    ```
    A.  os.popen
    B.  os.fork
    C.  os.system
    D.  os.link
    ```

18. 文件内容实例如下

    ```
    192.168.0.20--[0B/Sep/2015:20:05:30+0800] "GET /android/login/?method=get_server HTTP/1.1" -200 22268 "-" "-" "-" 0.055 0.139
    
    请写出命令行下(shell 默认bash), 提取请求时间($request_time) 大于0.1秒的请求($request), 并写入access_long_time.log文件中的命令
    ```

19. 你最熟悉的unix环境是?

20. 你最熟悉的unix环境是

21. unix下查询环境变量的命令是

22. 查询脚本定时任务的命令是

23. Apache服务器默认的接听连接端口号是

    ```
    A.  1024
    B.  800
    C.  80
    D.  8
    ```

24. 建立一个新文件可以使用的命令为

    ```
    A.  chmod
    B.  more
    C.  cp
    D.  touch
    ```

25. /etc/ethX表示

    ```
    A.  系统会送接口
    B.  以太网接口设备
    C.  令牌环网设备
    D.  PPP设备
    ```

26. 显示用户的ID, 以及所属组的ID, 要使用的命令是

    ```
    A.  su
    B.  who
    C.  id
    D.  man
    ```

27. 显示用户的ID, 以及所属组的ID, 要使用的命令是

    ```
    A.  su
    B.  who
    C.  id
    D.  man
    ```

28. 为了修改文件test的许可模式, 使其文件属性具有读写和运行的权限, 组和其他用户可以读和运行, 可以采用

    ```
    A.  chmod 755 test
    B.  chmod 700 test
    C.  chmod +rwx test
    D.  chmod g-w test
    ```

29. 取ls -l 输出结果的第5列的值的正确写法是

    ```
    A.  ls -l |awk "{print$5}"
    B.  ls -l |awk '{print$5}'
    C.  ls -l |awk {print$5}
    D.  ls -l |awk 'print$5'
    ```

30. 什么命令解压缩tar.gz文件

    ```
    A.  tar -czcf filename.tar.gz
    B.  tar -xzvf filename.tar.gz
    C.  tar -tzvf filename.tar.gz
    D.  tar -dzvf filename.tar.gz
    ```

31. 以下哪个命令是vi编辑器中执行存盘退出的

    ```
    A.  q
    B.  zz
    C.  :q!
    D.  :wq
    ```

32. 简述 saltstack、ansible、fabric、puppet工具的作用？

33. uwsgi和cgi的区别？

34. supervisor的作用？

35. 解释 PV、UV 的含义？

36. 解释 QPS的含义？

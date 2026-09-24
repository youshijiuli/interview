# ftp文件传输系统


## 功能需求


1. 用户认证
    - configparser：存配置文件
    - hashlib模块：加密解密匹配密码账户
2. 多用户（暂时不用）
3. 每个用户有自己的家目录
4. 用户可以在自己的家目录 进行目录切换
5. dir 用户可以查看当前目录的文件列表，文件名，文件大小
6. get file
7. put file 进度条展示
8. del file
9. mkdir dir

````python
hasattr
getattr(self, "funame")
setattr(self, "func", var)
delattr
````


## 功能拓展

断点续传

1. 检查是否有未传输完的文件

- 如果有，提示是否续传
    + 把文件名+大小发给服务端
    + 服务端 按照客户端 数据找到文件
        - 如果找不到，返回错误
        - 找到了，返回准备发送的消息
        - Seek 到指定位置，开始发送

2. 记录传的是什么文件
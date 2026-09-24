# 局域网FTP文件交互工具

一个简单易用的FTP客户端工具，用于在局域网内与FTP服务器进行文件交互。

## 功能特点

- 连接局域网内的FTP服务器
- 浏览远程目录结构
- 上传文件到FTP服务器
- 从FTP服务器下载文件
- 创建、删除远程目录
- 删除远程文件
- 可视化界面，操作直观

## 安装要求

- Python 3.6+
- 以下Python库：
  - tkinter
  - ftplib
  - os
  - sys

## 安装方法

```bash
# 克隆仓库
git clone https://github.com/yourusername/lan-ftp-tool.git

# 进入项目目录
# 安装依赖
pip install -r requirements.txt
```

## 使用方法

1. 运行主程序：

```bash
python ftp_client.py
```

2. 在界面中输入FTP服务器信息：
   - 服务器地址
   - 端口号（默认为21）
   - 用户名
   - 密码

3. 点击"连接"按钮，连接到FTP服务器

4. 连接成功后，可以浏览远程目录、上传和下载文件

## 界面说明

- 左侧面板：显示本地文件系统
- 右侧面板：显示远程FTP服务器的文件系统
- 中间按钮：
  - "→"：上传选中的本地文件到远程服务器
  - "←"：下载选中的远程文件到本地

## 许可证

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件 
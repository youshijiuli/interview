# Linux 命令速查手册

> 高频命令、常用选项与实战示例，按功能分类整理。适用于日常开发、运维与面试复习。

---

## 文件与目录

### ls

列出目录内容，最常用的文件查看命令

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-l` | 长格式显示（权限、属主、大小、时间） |
| `-a` | 显示所有文件，含隐藏文件（. 开头） |
| `-h` | 与 -l 配合，以 K/M/G 显示人性化大小 |
| `-t` | 按修改时间排序（最新在前） |
| `-r` | 倒序排列 |
| `-R` | 递归列出子目录 |
| `-S` | 按文件大小排序 |

**示例：**

```bash
# 以长格式显示当前目录，含隐藏文件、人性化大小
ls -lah
# 按修改时间排序，快速找到最近改动的文件
ls -lt
# 递归查看 src 目录下的所有文件
ls -R src
```

### cd

切换工作目录

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `..` | 回到上一级目录 |
| `-` | 回到上一次所在的目录 |
| `~` | 回到当前用户的家目录 |

**示例：**

```bash
# 进入 /var/log 目录
cd /var/log
# 返回上一级目录
cd ..
# 回到上次所在目录（来回切换很实用）
cd -
```

### pwd

打印当前工作目录的绝对路径

**示例：**

```bash
# 显示当前所在目录，例如 /home/user/project
pwd
```

### mkdir

创建目录

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-p` | 递归创建多级目录，不存在则一并创建 |
| `-m` | 创建时直接指定权限，如 -m 755 |

**示例：**

```bash
# 创建单个目录 project
mkdir project
# 递归创建 a/b/c 三层目录
mkdir -p a/b/c
# 创建权限为 700 的目录
mkdir -m 700 private
```

### touch

创建空文件，或更新已有文件的时间戳

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-t` | 指定时间戳，如 -t 202401011200 |
| `-a` | 仅更新访问时间 |
| `-m` | 仅更新修改时间 |

**示例：**

```bash
# 创建一个空的 readme.md 文件
touch readme.md
# 把 file 的时间戳设为 2024-01-01 12:00
touch -t 202401011200 file
```

### cp

复制文件或目录

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-r` | 递归复制目录 |
| `-a` | 归档复制，保留权限、属主、时间等属性 |
| `-i` | 覆盖前询问确认 |
| `-v` | 显示复制过程 |
| `-u` | 仅复制源更新、目标不存在的文件 |

**示例：**

```bash
# 递归复制 src 目录到 dst
cp -r src/ dst/
# 复制一份备份文件
cp config.yaml config.yaml.bak
# 归档模式备份目录，保留属性并显示过程
cp -av data/ /backup/data/
```

### mv

移动文件，或重命名

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-i` | 覆盖前询问 |
| `-v` | 显示移动过程 |
| `-u` | 仅当源较新时才移动 |

**示例：**

```bash
# 重命名文件
mv old.txt new.txt
# 把所有 .log 文件移动到 ~/logs/
mv *.log ~/logs/
# 移动前若有同名文件会询问确认
mv -i file.txt /tmp/
```

### rm

删除文件或目录。删除不可恢复，务必谨慎

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-r` | 递归删除目录及其内容 |
| `-f` | 强制删除，不询问、忽略不存在的文件 |
| `-i` | 逐个询问确认 |
| `-v` | 显示删除过程 |

**示例：**

```bash
# 强制递归删除 build 目录
rm -rf build/
# 逐个确认后删除 .tmp 文件
rm -i *.tmp
# 删除单个文件
rm file.txt
```

### ln

创建链接：硬链接或符号链接（快捷方式）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-s` | 创建符号链接（软链接），跨文件系统、可指向目录 |
| `-f` | 若目标已存在则强制覆盖 |

**示例：**

```bash
# 创建指向 python3 的软链接 python
ln -s /usr/bin/python3 python
# 为目录创建快捷方式
ln -s /mnt/data ~/data-link
# 创建硬链接（同一文件的两个名字）
ln backup.txt backup-hard
```

### find

在目录树中按条件查找文件

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-name` | 按文件名匹配（支持通配符） |
| `-type` | 按类型：f 文件 / d 目录 / l 链接 |
| `-size` | 按大小，如 +100M、-10k |
| `-mtime` | 按修改时间（天），如 -mtime -7 表示 7 天内 |
| `-maxdepth` | 限制搜索深度 |
| `-exec` | 对结果执行命令，{} 为占位符 |

**示例：**

```bash
# 在当前目录递归查找所有 Python 文件
find . -name "*.py"
# 查找 /var 下大于 100M 的文件
find /var -type f -size +100M
# 查找最近 7 天内修改过的 .log 文件
find . -mtime -7 -name "*.log"
# 查找并删除所有 .tmp 文件
find . -name "*.tmp" -exec rm {} \;
```

### tree

以树状图显示目录结构

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-L` | 限制层级深度，如 -L 2 |
| `-d` | 只显示目录不显示文件 |
| `-a` | 显示隐藏文件 |

**示例：**

```bash
# 显示两层目录结构
tree -L 2
# 只看目录结构，忽略文件
tree -d
```

### file

识别文件的类型

**示例：**

```bash
# 输出：gzip compressed data，确认压缩格式
file archive.tar.gz
# 显示 ELF 可执行文件等类型信息
file /bin/ls
```

## 文本处理

### cat

查看文件内容、合并文件

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-n` | 显示行号 |
| `-b` | 只给非空行编号 |
| `-A` | 显示不可见字符（行尾 $ 等） |

**示例：**

```bash
# 把文件内容打印到终端
cat config.yaml
# 合并两个文件到 c.txt
cat a.txt b.txt > c.txt
# 带行号查看脚本内容
cat -n script.sh
```

### less

分页查看大文件，支持前后翻页与搜索

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `/pattern` | 在文件内搜索，按 n 跳到下一个 |
| `q` | 退出 |
| `g / G` | 跳到文件开头 / 结尾 |
| `-N` | 显示行号 |

**示例：**

```bash
# 分页查看系统日志
less /var/log/syslog
# 带行号分页查看日志
less -N app.log
```

### head

查看文件开头部分，默认前 10 行

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-n` | 指定行数 |
| `-c` | 按字节数查看 |

**示例：**

```bash
# 查看日志前 20 行
head -n 20 access.log
# 查看文件前 100 字节
head -c 100 file.bin
```

### tail

查看文件结尾部分，默认后 10 行；-f 实时跟踪

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-n` | 指定行数 |
| `-f` | 实时跟踪文件新增内容（Ctrl+C 退出） |
| `-F` | 跟踪并自动处理文件被重建的情况 |

**示例：**

```bash
# 查看日志最后 50 行
tail -n 50 app.log
# 实时滚动查看日志（排查问题时最常用）
tail -f app.log
```

### grep

按正则搜索文本，Linux 文本处理之王

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-r` | 递归搜索目录下的所有文件 |
| `-i` | 忽略大小写 |
| `-n` | 显示匹配行号 |
| `-v` | 反向匹配（排除） |
| `-E` | 使用扩展正则（等价 egrep） |
| `-l` | 只列出包含匹配的文件名 |
| `-c` | 只统计匹配的行数 |

**示例：**

```bash
# 递归搜索 src 下所有包含 TODO 的行
grep -rn "TODO" src/
# 在进程列表中过滤出 nginx 进程
ps aux | grep nginx
# 过滤掉注释行，查看有效配置
grep -v "^#" nginx.conf
# 扩展正则，匹配 error 或 failed
grep -E "error|failed" *.log
```

### sed

流编辑器，批量替换、删除、插入文本

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `s/old/new/g` | 全局替换 old 为 new |
| `-i` | 直接修改文件（而非仅输出） |
| `/pattern/d` | 删除匹配行 |
| `-n '5,10p'` | 只打印第 5 到 10 行 |

**示例：**

```bash
# 就地替换文件中的 foo 为 bar
sed -i 's/foo/bar/g' file.txt
# 删除以 # 开头的注释行（仅输出）
sed '/^#/d' config.conf
# 打印大文件的前 20 行
sed -n '1,20p' big.log
```

### awk

强大的文本分析语言，按列处理

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `'{print $1}'` | 按空格/制表符分隔，打印第 1 列 |
| `-F:` | 指定分隔符为冒号 |
| `'{print $NF}'` | $NF 表示最后一列 |

**示例：**

```bash
# 提取每行第一个字段
awk '{print $1}' data.txt
# 按冒号分隔，提取用户名和 UID
awk -F: '{print $1, $3}' /etc/passwd
# 从 free 输出中取出可用内存列
free -h | awk 'NR==2{print $4}'
```

### sort

对文本行排序

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-n` | 按数值排序 |
| `-r` | 倒序 |
| `-k` | 按第几列排序 |
| `-u` | 去重（只保留唯一行） |

**示例：**

```bash
# 按数值倒序排序
sort -nr scores.txt
# 按第 2 列排序
sort -k2,2 data.txt
# 对历史命令去重排序
history | sort -u
```

### uniq

去除相邻重复行，常与 sort 搭配

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-c` | 统计每行出现次数 |
| `-d` | 只显示重复行 |
| `-u` | 只显示不重复的行 |

**示例：**

```bash
# 统计每行出现的次数
sort log.txt | uniq -c
# 统计 IP 出现次数并倒序（Top 排行）
sort ips.txt | uniq -c | sort -nr
```

### wc

统计行数、单词数、字节数

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-l` | 只统计行数 |
| `-w` | 只统计单词数 |
| `-c` | 只统计字节数 |

**示例：**

```bash
# 统计文件行数
wc -l file.txt
# 统计进程总数（减 1 为实际进程数）
ps aux | wc -l
```

### cut

按分隔符或位置截取文本列

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-d` | 指定分隔符 |
| `-f` | 取第几列（配合 -d） |
| `-c` | 按字符位置截取 |

**示例：**

```bash
# 提取 passwd 文件第一列（用户名）
cut -d: -f1 /etc/passwd
# 截取每行前 10 个字符
cut -c1-10 file.txt
```

### tr

字符转换、删除、压缩

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `'a-z' 'A-Z'` | 把小写转大写 |
| `-d` | 删除指定字符 |
| `-s` | 压缩连续重复字符 |

**示例：**

```bash
# 输出 HELLO
echo hello | tr 'a-z' 'A-Z'
# 删除 Windows 行尾的 \r 字符
cat file | tr -d '\r'
# 把连续空格压缩为单个空格
cat file | tr -s ' '
```

### diff

逐行比较两个文件差异

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-u` | 统一格式输出（最常用） |
| `-r` | 递归比较目录 |
| `-y` | 并排显示差异 |

**示例：**

```bash
# 以统一格式查看文件差异
diff -u old.txt new.txt
# 递归比较两个目录
diff -r dir1/ dir2/
```

### xargs

把前一个命令的输出作为参数传给后一个命令

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-n` | 每次传递的参数个数 |
| `-0` | 配合 find -print0 处理含空格/换行的文件名 |
| `-I` | 用占位符替换参数位置 |

**示例：**

```bash
# 删除所有 .tmp 文件
find . -name "*.tmp" | xargs rm
# 对每个 txt 文件分别统计行数
ls *.txt | xargs -n1 wc -l
# 依次创建 a、b、c 三个目录
echo a b c | xargs -n1 mkdir
```

### tee

同时把输出写到屏幕和文件

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-a` | 追加到文件而非覆盖 |

**示例：**

```bash
# 执行 cmd 并把输出同时保存到日志
cmd | tee output.log
# 追加模式记录输出
cmd | tee -a history.log
```

### echo

输出文本到终端

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-n` | 输出后不换行 |
| `-e` | 启用转义（\n 换行、\t 制表符） |

**示例：**

```bash
# 输出一行文本
echo "Hello World"
# 输出环境变量 PATH 的值
echo $PATH
# 分行输出 a 和 b
echo -e "a\nb"
```

## 权限与用户

### chmod

修改文件/目录权限（读 4 写 2 执行 1）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `755` | 属主 rwx、组 r-x、其他 r-x（常用目录） |
| `644` | 属主 rw-、组 r--、其他 r--（常用文件） |
| `+x` | 给所有角色加执行权限 |
| `-R` | 递归修改目录内所有文件 |

**示例：**

```bash
# 属主可读写执行，其他人可读可执行
chmod 755 script.sh
# 给脚本加执行权限
chmod +x script.sh
# 递归把目录内文件改为 644
chmod -R 644 /var/www/static
```

### chown

修改文件/目录的属主与属组

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `user:group` | 同时修改属主和属组 |
| `-R` | 递归修改 |

**示例：**

```bash
# 把文件属主改为 dev，属组改为 dev
chown dev:dev file.txt
# 递归修改 web 目录属主
chown -R www-data:www-data /var/www
```

### chgrp

修改文件/目录的属组

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-R` | 递归修改 |

**示例：**

```bash
# 把 project 目录的属组改为 dev
chgrp dev project/
```

### umask

查看/设置新建文件的默认权限掩码

**示例：**

```bash
# 查看当前掩码，如 0022（新文件默认 644、目录 755）
umask
# 设置更严格的默认权限
umask 0027
```

### su

切换用户身份

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-` | 以登录 shell 方式切换（加载目标用户环境） |
| `-c` | 以目标用户执行单条命令 |

**示例：**

```bash
# 切换到 root（会加载 root 的环境变量）
su - root
# 以 www-data 身份执行命令
su -c "systemctl status nginx" www-data
```

### sudo

以其他用户（默认 root）权限执行命令

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-i` | 以 root 登录 shell 进入（可长期提权） |
| `-u` | 以指定用户执行，如 -u www-data |
| `-E` | 保留当前环境变量 |

**示例：**

```bash
# 以 root 权限更新软件源
sudo apt update
# 以 www-data 用户创建文件
sudo -u www-data touch /var/www/a.txt
# 切换到 root 交互 shell
sudo -i
```

### useradd

创建新用户

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-m` | 同时创建家目录 |
| `-s` | 指定登录 shell，如 -s /bin/bash |
| `-G` | 指定附加组 |

**示例：**

```bash
# 创建用户 alice 并生成家目录
sudo useradd -m -s /bin/bash alice
# 创建用户并加入 dev 组
sudo useradd -m -G dev alice
```

### usermod

修改用户属性

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-aG` | 把用户追加到附加组（-a 防止覆盖已有组） |
| `-l` | 修改用户名 |
| `-s` | 修改登录 shell |

**示例：**

```bash
# 把 alice 加入 sudo 组（授予提权权限）
sudo usermod -aG sudo alice
# 把 alice 的 shell 改为 zsh
sudo usermod -s /bin/zsh alice
```

### passwd

修改用户密码

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `user` | 修改指定用户密码（需 root） |
| `-l / -u` | 锁定 / 解锁账号 |

**示例：**

```bash
# 修改当前用户密码
passwd
# root 修改 alice 的密码
sudo passwd alice
# 锁定 alice 账号
sudo passwd -l alice
```

### id

查看用户 ID、组 ID 与所属组

**示例：**

```bash
# 查看当前用户身份信息
id
# 查看 alice 的 UID、GID 及所属组
id alice
```

### whoami

打印当前有效用户名

**示例：**

```bash
# 输出当前用户名，如 dev
whoami
```

## 进程管理

### ps

查看进程快照

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `aux` | 显示所有进程（含其他用户），带 CPU/内存占用 |
| `-ef` | 全格式显示所有进程 |
| `-C` | 按命令名查找进程 |
| `--sort` | 按字段排序，如 --sort=-%mem |

**示例：**

```bash
# 查看 nginx 相关进程及资源占用
ps aux | grep nginx
# 以树状结构显示进程父子关系
ps -ef --forest
# 查看 CPU 占用最高的 10 个进程
ps aux --sort=-%cpu | head -10
```

### top

实时查看系统进程与资源占用（htop 是其增强版）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `P / M` | 按 CPU / 内存排序 |
| `k` | 杀死指定进程 |
| `-d` | 设置刷新间隔秒数 |

**示例：**

```bash
# 进入实时监控界面，按 q 退出
top
# 每 2 秒刷新一次
top -d 2
```

### htop

top 的交互式增强版，操作更直观

**示例：**

```bash
# 彩色交互界面，F5 树状视图、F9 杀进程
htop
```

### kill

向进程发送信号（默认 SIGTERM 优雅终止）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-9` | SIGKILL 强制杀死（无法被捕获） |
| `-15` | SIGTERM 请求终止（默认） |
| `-l` | 列出所有信号名 |

**示例：**

```bash
# 请求进程 1234 优雅退出
kill -15 1234
# 强制杀死进程 1234（慎用）
kill -9 1234
# 列出全部信号
kill -l
```

### pkill

按名称/特征批量终止进程

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-f` | 按完整命令行匹配 |
| `-9` | 强制终止 |
| `-u` | 按属主匹配 |

**示例：**

```bash
# 按命令行特征杀掉 node 服务
pkill -f "node server.js"
# 强制杀掉 bob 的所有进程
pkill -9 -u bob
```

### killall

按进程名终止所有同名进程

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-9` | 强制终止 |
| `-i` | 逐个确认 |

**示例：**

```bash
# 强制终止所有 java 进程
killall -9 java
# 终止所有 nginx 进程
killall nginx
```

### jobs / fg / bg

作业控制：查看、前台/后台切换任务

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `Ctrl+Z` | 把当前前台任务挂起到后台 |
| `jobs` | 列出后台任务 |
| `fg %1` | 把作业 1 调回前台 |
| `bg %1` | 让作业 1 在后台继续运行 |

**示例：**

```bash
# 直接在后台运行命令
cmd &
# 查看当前 shell 的后台任务列表
jobs
# 把编号为 1 的作业切回前台
fg %1
```

### nohup

让命令忽略挂断信号，退出终端后仍运行

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `&` | 后台运行 |
| `2>&1` | 把错误输出也重定向到日志 |

**示例：**

```bash
# 后台启动服务，退出终端也不中断
nohup ./server.sh > app.log 2>&1 &
# 后台运行 Python 程序
nohup python app.py &
```

### nice / renice

调整进程优先级（-20 最高，19 最低）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-n` | nice 启动时指定优先级 |
| `-p` | renice 按 PID 调整 |

**示例：**

```bash
# 以较低优先级启动任务，避免影响其他进程
nice -n 10 ./heavy-task
# 提高进程 1234 的优先级
renice -5 -p 1234
```

### watch

周期性重复执行命令并刷新显示

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-n` | 刷新间隔秒数 |
| `-d` | 高亮两次输出间的差异 |

**示例：**

```bash
# 每 2 秒刷新一次内存占用
watch -n 2 free -h
# 监控目录变化并高亮差异
watch -d "ls -la"
```

### pgrep

按名称查找进程 PID

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-l` | 同时显示进程名 |
| `-f` | 按完整命令行匹配 |
| `-u` | 按用户筛选 |

**示例：**

```bash
# 查找 nginx 进程及其 PID
pgrep -l nginx
# 按命令行特征查找 java 应用
pgrep -f "java.*app"
```

## 系统信息

### uname

查看内核与系统架构信息

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-a` | 显示全部信息 |
| `-r` | 显示内核版本 |
| `-m` | 显示机器架构（x86_64 等） |

**示例：**

```bash
# 查看完整系统内核信息
uname -a
# 查看架构（判断是 amd64 还是 arm64）
uname -m
```

### uptime

查看系统运行时间与负载

**示例：**

```bash
# 显示运行时长、登录用户数与 1/5/15 分钟平均负载
uptime
```

### free

查看内存使用情况

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-h` | 人性化单位显示 |
| `-s` | 周期刷新，如 -s 3 |

**示例：**

```bash
# 查看内存与 Swap 使用情况
free -h
# 每 3 秒刷新一次内存信息
free -h -s 3
```

### df

查看磁盘分区空间使用情况

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-h` | 人性化单位 |
| `-T` | 显示文件系统类型 |
| `-i` | 查看 inode 使用情况 |

**示例：**

```bash
# 查看所有分区的空间使用
df -h
# 带文件系统类型查看（ext4、xfs 等）
df -hT
```

### du

统计目录/文件占用磁盘大小

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-sh` | 汇总目录总大小（人性化） |
| `--max-depth` | 限制统计深度 |
| `-h` | 人性化单位 |

**示例：**

```bash
# 统计当前目录下每个项目的大小
du -sh *
# 统计一级子目录大小
du -h --max-depth=1 .
# 查看缓存目录总大小
du -sh ~/.cache
```

### date

显示或设置系统日期时间

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `+%F` | 按 YYYY-MM-DD 格式输出 |
| `+%T` | 按 HH:MM:SS 格式输出 |
| `-s` | 设置时间（需 root） |

**示例：**

```bash
# 显示当前日期时间
date
# 按自定义格式输出时间
date '+%Y-%m-%d %H:%M:%S'
# 输出 Unix 时间戳
date +%s
```

### cal

显示日历

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-y` | 显示全年日历 |
| `3 2025` | 显示某年某月 |

**示例：**

```bash
# 显示本月日历
cal
# 显示 2025 年全年日历
cal 2025
```

### hostname

查看或设置主机名

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-I` | 显示本机所有 IP 地址 |

**示例：**

```bash
# 查看主机名
hostname
# 快速查看本机 IP
hostname -I
```

### lscpu

查看 CPU 架构信息

**示例：**

```bash
# 查看 CPU 型号、核心数、架构等
lscpu
# 只看 CPU 型号
lscpu | grep "Model name"
```

### history

查看命令历史

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-c` | 清空历史 |
| `!n` | 执行历史中第 n 条命令 |
| `!!` | 执行上一条命令 |

**示例：**

```bash
# 列出当前 shell 的命令历史
history
# 在历史中搜索 ssh 相关命令
history | grep ssh
# 再次执行上一条命令
!!
```

### which

查找可执行命令的路径

**示例：**

```bash
# 输出 python3 所在路径，如 /usr/bin/python3
which python3
# 列出所有匹配的 node 路径
which -a node
```

### whereis

查找命令的二进制、源码与手册位置

**示例：**

```bash
# 显示 nginx 的可执行文件、配置与手册路径
whereis nginx
```

### env

查看或设置环境变量

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `\| grep` | 配合过滤查找指定变量 |

**示例：**

```bash
# 列出全部环境变量
env
# 查看 PATH 变量内容
env | grep PATH
```

## 网络

### ping

测试网络连通性与延迟

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-c` | 指定发送次数 |
| `-i` | 发送间隔秒数 |
| `-4 / -6` | 强制 IPv4 / IPv6 |

**示例：**

```bash
# 向目标发送 4 个探测包
ping -c 4 baidu.com
# 每 0.5 秒探测一次内网网关
ping -i 0.5 192.168.1.1
```

### curl

命令行 HTTP/HTTPS 请求工具，接口调试必备

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-I` | 只获取响应头 |
| `-o` | 保存响应到文件 |
| `-L` | 跟随重定向 |
| `-X` | 指定请求方法，如 -X POST |
| `-H` | 添加请求头 |
| `-d` | 发送 POST 数据 |
| `-s` | 静默模式（不显示进度与错误） |

**示例：**

```bash
# 获取响应头信息
curl -I https://example.com
# 跟随重定向下载文件
curl -o file.zip -L https://example.com/file.zip
# 发送 JSON POST 请求
curl -X POST -H "Content-Type: application/json" -d '{"k":1}' https://api.example.com/v1
# 静默请求健康检查接口
curl -s https://api.example.com/health
```

### wget

命令行下载工具，支持断点续传

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-c` | 断点续传 |
| `-O` | 指定保存文件名 |
| `-q` | 静默模式 |
| `-r` | 递归下载 |

**示例：**

```bash
# 下载文件到当前目录
wget https://example.com/pkg.tar.gz
# 断点续传大文件
wget -c https://example.com/big.iso
# 自定义保存文件名
wget -O my.tar.gz https://example.com/pkg.tar.gz
```

### ssh

安全远程登录服务器

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-p` | 指定端口 |
| `-i` | 指定私钥文件 |
| `-L` | 本地端口转发 |
| `-N` | 不执行命令（仅建立隧道） |

**示例：**

```bash
# 默认端口 22 登录远程主机
ssh user@192.168.1.10
# 指定端口与密钥登录
ssh -p 2222 -i ~/.ssh/id_ed25519 user@host
# 把本地 8080 转发到远程的 80 端口
ssh -L 8080:localhost:80 user@host
```

### scp

基于 SSH 的远程文件复制

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-r` | 递归复制目录 |
| `-P` | 指定端口（注意大写） |
| `-i` | 指定密钥 |

**示例：**

```bash
# 上传文件到远程 /tmp
scp file.txt user@host:/tmp/
# 递归上传目录
scp -r project/ user@host:~/
# 从远程下载文件到本地
scp user@host:/var/log/app.log ./
```

### rsync

高效同步/备份工具，支持增量传输

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-a` | 归档模式（递归并保留属性） |
| `-v` | 显示详细过程 |
| `-z` | 传输时压缩 |
| `--delete` | 删除目标端多余文件（与源保持一致） |
| `-e ssh` | 通过 SSH 传输 |

**示例：**

```bash
# 增量备份到远程
rsync -avz ./src user@host:/backup/src
# 本地同步并删除多余文件
rsync -av --delete src/ dst/
# 指定 SSH 端口同步
rsync -avz -e "ssh -p 2222" ./ user@host:~/
```

### ip

现代网络配置命令（替代 ifconfig）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `addr` | 查看/配置 IP 地址 |
| `link` | 查看/配置网络接口 |
| `route` | 查看/配置路由表 |

**示例：**

```bash
# 查看所有网卡及 IP 地址
ip addr
# 查看路由表（默认网关）
ip route show
# 启用 eth0 网卡
ip link set eth0 up
```

### ifconfig

查看/配置网络接口（传统命令，部分发行版需安装 net-tools）

**示例：**

```bash
# 查看所有网卡信息
ifconfig
# 手动配置静态 IP
sudo ifconfig eth0 192.168.1.5 netmask 255.255.255.0
```

### netstat

查看网络连接、端口监听与路由

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-tulnp` | 查看监听端口及对应进程（最常用） |
| `-i` | 查看网卡统计 |
| `-r` | 查看路由表 |

**示例：**

```bash
# 查看所有监听端口与进程
netstat -tulnp
# 确认 8080 端口被哪个进程占用
netstat -tulnp | grep 8080
```

### ss

socket 统计，netstat 的现代替代，速度更快

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-t` | TCP 连接 |
| `-u` | UDP 连接 |
| `-l` | 只显示监听端口 |
| `-n` | 以数字显示端口 |
| `-p` | 显示进程 |

**示例：**

```bash
# 查看所有监听端口与进程
ss -tulnp
# 查看已建立的 TCP 连接
ss -tn state established
```

### traceroute

追踪数据包到达目标的路径

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-n` | 不解析域名（更快） |
| `-m` | 最大跳数 |

**示例：**

```bash
# 追踪到百度的网络路径
traceroute baidu.com
# 以 IP 形式快速追踪
traceroute -n 8.8.8.8
```

### dig

DNS 查询工具，排查域名解析问题

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `+short` | 简洁输出 |
| `-x` | 反向查询（IP 查域名） |
| `@8.8.8.8` | 指定 DNS 服务器查询 |

**示例：**

```bash
# 查询 A 记录完整信息
dig example.com
# 只输出解析结果 IP
dig example.com +short
# 反向解析 8.8.8.8
dig -x 8.8.8.8
```

### nslookup

DNS 查询工具（传统命令）

**示例：**

```bash
# 查询域名解析结果
nslookup example.com
```

### nc

瑞士军刀：端口探测、监听、传输

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-z` | 只扫描端口不发送数据 |
| `-v` | 显示详细信息 |
| `-l` | 监听模式 |
| `-p` | 监听端口 |

**示例：**

```bash
# 探测目标 22 端口是否开放
nc -zv host 22
# 在本机 8080 端口监听（调试 webhook）
nc -l -p 8080
# 快速探测 80 和 443 端口
nc -zv -w3 example.com 80 443
```

## 磁盘与存储

### lsblk

以树状列出块设备（硬盘、分区）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-f` | 显示文件系统类型与 UUID |
| `-m` | 显示属主与权限 |

**示例：**

```bash
# 查看磁盘与分区结构
lsblk
# 查看分区文件系统类型与 UUID
lsblk -f
```

### fdisk

磁盘分区管理工具

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-l` | 列出所有磁盘及分区表 |
| `/dev/sda` | 进入交互式分区操作（m 查看帮助） |

**示例：**

```bash
# 列出所有磁盘分区
sudo fdisk -l
# 对 /dev/sdb 进行分区操作
sudo fdisk /dev/sdb
```

### parted

高级分区工具，支持 GPT 与更大容量

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `print` | 显示分区表 |
| `mkpart` | 创建分区 |
| `rm` | 删除分区 |

**示例：**

```bash
# 查看 sda 的分区表
sudo parted /dev/sda print
# 把磁盘初始化为 GPT 分区表
sudo parted -s /dev/sdb mklabel gpt
```

### blkid

查看块设备的 UUID 与文件系统类型

**示例：**

```bash
# 列出所有分区的 UUID（写 fstab 时常用）
sudo blkid
# 查看单个分区的 UUID
blkid /dev/sdb1
```

### mkfs

格式化分区为指定文件系统

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-t` | 指定类型：ext4 / xfs / vfat 等 |
| `-L` | 设置卷标 |

**示例：**

```bash
# 把分区格式化为 ext4（数据会被清空）
sudo mkfs.ext4 /dev/sdb1
# 格式化为 xfs 文件系统
sudo mkfs -t xfs /dev/sdb1
```

### mount / umount

挂载 / 卸载文件系统

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-t` | 指定文件系统类型 |
| `-o` | 挂载选项，如 ro、noexec |
| `-a` | 挂载 fstab 中所有条目 |

**示例：**

```bash
# 把分区挂载到 /mnt
sudo mount /dev/sdb1 /mnt
# 挂载 NFS 网络共享
sudo mount -t nfs server:/share /mnt/nfs
# 卸载 /mnt 上的文件系统
sudo umount /mnt
```

### fsck

检查并修复文件系统（需先卸载）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-f` | 强制检查 |
| `-y` | 对修复询问自动回答 yes |

**示例：**

```bash
# 强制检查分区文件系统
sudo fsck -f /dev/sdb1
# 自动修复检查出的问题
sudo fsck -y /dev/sda1
```

## 软件包管理

### apt

Debian/Ubuntu 软件包管理器（现代前端）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `update` | 更新软件源索引 |
| `upgrade` | 升级所有可升级软件包 |
| `install` | 安装软件包 |
| `remove` | 卸载软件包 |
| `search` | 搜索软件包 |
| `show` | 查看软件包详情 |

**示例：**

```bash
# 刷新软件源
sudo apt update
# 安装 nginx
sudo apt install -y nginx
# 升级系统软件包
sudo apt upgrade
# 搜索 python3 相关包
apt search python3
# 卸载 nginx
sudo apt remove nginx
```

### apt-get

Debian/Ubuntu 软件包管理器的传统命令

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `install` | 安装 |
| `autoremove` | 自动移除不再需要的依赖 |
| `dist-upgrade` | 智能升级（含依赖变更） |

**示例：**

```bash
# 安装 git
sudo apt-get install -y git
# 清理无用依赖
sudo apt-get autoremove
```

### dpkg

Debian 底层包管理，直接操作 .deb 包

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-i` | 安装 .deb 包 |
| `-r` | 卸载包（保留配置） |
| `-l` | 列出已安装包 |
| `-S` | 查询文件属于哪个包 |

**示例：**

```bash
# 安装本地 deb 包
sudo dpkg -i package.deb
# 查看 nginx 是否已安装
dpkg -l | grep nginx
# 查询 ls 命令属于哪个软件包
dpkg -S /bin/ls
```

### yum

RHEL/CentOS 传统软件包管理器

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `install` | 安装 |
| `remove` | 卸载 |
| `update` | 升级 |
| `search` | 搜索 |
| `list installed` | 列出已安装包 |

**示例：**

```bash
# 安装 httpd
sudo yum install -y httpd
# 升级系统
sudo yum update
# 搜索 nginx 包
yum search nginx
```

### dnf

Fedora/RHEL 8+ 新一代软件包管理器（yum 替代）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `install` | 安装 |
| `remove` | 卸载 |
| `update` | 升级 |
| `search` | 搜索 |
| `info` | 查看包信息 |

**示例：**

```bash
# 安装 git
sudo dnf install -y git
# 升级系统
sudo dnf update
# 搜索软件包
dnf search python3
```

### pacman

Arch Linux 软件包管理器

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-S` | 安装/搜索（-Ss 搜索、-Syu 升级） |
| `-R` | 卸载（-Rns 连同依赖与配置） |
| `-Q` | 查询已安装包（-Qs 搜索本地包） |

**示例：**

```bash
# 安装 vim
sudo pacman -S vim
# 同步并升级整个系统
sudo pacman -Syu
# 在仓库搜索 docker
pacman -Ss docker
# 卸载 docker 及其依赖
sudo pacman -Rns docker
```

### snap

Ubuntu 的沙箱化软件包格式

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `install` | 安装 |
| `remove` | 卸载 |
| `list` | 列出已安装 snap |

**示例：**

```bash
# 安装 VS Code
sudo snap install code --classic
# 查看已安装的 snap 应用
snap list
```

## 压缩与归档

### tar

最常用的打包/压缩工具（tar.gz 等）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-czvf` | 创建 tar.gz 压缩包 |
| `-xzvf` | 解压 tar.gz |
| `-tzf` | 查看压缩包内容 |
| `-C` | 解压到指定目录 |
| `--exclude` | 排除文件 |

**示例：**

```bash
# 把 project 目录打包压缩为 tar.gz
tar -czvf backup.tar.gz project/
# 解压到 /tmp 目录
tar -xzvf backup.tar.gz -C /tmp
# 不解压查看包内文件列表
tar -tzvf backup.tar.gz
# 打包并排除 log 文件
tar -czvf data.tar.gz --exclude='*.log' data/
```

### gzip / gunzip

gzip 压缩 / 解压单个文件

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-d` | 解压（等价 gunzip） |
| `-k` | 保留原文件 |
| `-9` | 最高压缩率 |

**示例：**

```bash
# 压缩为 app.log.gz
gzip app.log
# 压缩且保留原文件
gzip -dk app.log
# 解压恢复原文件
gunzip app.log.gz
```

### bzip2 / bunzip2

更高压缩率的压缩工具

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-d` | 解压 |
| `-k` | 保留原文件 |

**示例：**

```bash
# 压缩为 bigfile.bz2
bzip2 bigfile
# 解压恢复
bunzip2 bigfile.bz2
```

### xz

高压缩率工具（LZMA 算法）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-d` | 解压 |
| `-k` | 保留原文件 |
| `-9` | 最高压缩级别 |

**示例：**

```bash
# 压缩为 file.tar.xz
xz file.tar
# 解压并保留压缩包
xz -dk file.tar.xz
```

### zip / unzip

处理 zip 格式（与 Windows 兼容）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-r` | zip 递归压缩目录 |
| `-d` | unzip 解压到指定目录 |
| `-l` | unzip 查看内容列表 |

**示例：**

```bash
# 压缩目录为 zip
zip -r archive.zip project/
# 解压到 /tmp
unzip archive.zip -d /tmp
# 查看 zip 包内容
unzip -l archive.zip
```

### zcat / zless

不解压直接查看 gzip 文件内容

**示例：**

```bash
# 直接查看 gz 日志的前几行
zcat access.log.gz | head
# 分页查看 gz 日志
zless app.log.gz
```

## shell 与技巧

### man

查看命令手册（最强大的学习工具）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-k` | 按关键词搜索手册 |
| `N` | 手册章节，如 man 5 passwd |

**示例：**

```bash
# 查看 ls 的完整手册
man ls
# 搜索与 copy 相关的手册页
man -k copy
# 查看 crontab 文件格式说明
man 5 crontab
```

### alias

设置命令别名（常用命令缩写）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `ll='ls -lah'` | 定义别名 |
| `-p` | 列出当前所有别名 |
| `unalias` | 删除别名 |

**示例：**

```bash
# 定义 ll 为长格式列表
alias ll='ls -lah'
# 让 grep 默认带颜色
alias grep='grep --color=auto'
# 查看已有别名
alias -p
```

### export

设置环境变量（对子进程生效）

**示例：**

```bash
# 把目录追加到 PATH
export PATH=$PATH:/usr/local/bin
# 设置 JAVA_HOME 环境变量
export JAVA_HOME=/usr/lib/jvm/java-17
```

### echo / printf

输出文本（printf 支持格式化输出）

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-n` | echo 不换行 |
| `-e` | echo 启用转义 |

**示例：**

```bash
# 输出家目录路径
echo $HOME
# 格式化输出并换行
printf "%s\n" hello
```

### sleep

延时指定秒数

**示例：**

```bash
# 等 5 秒后输出 done
sleep 5 && echo done
# 延时 1 分钟（m/h/d 分别表示分/时/天）
sleep 1m
```

### seq

生成数字序列

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `-w` | 等宽补零 |
| `-s` | 指定分隔符 |

**示例：**

```bash
# 生成 1 到 10
seq 1 10
# 生成 1、3、5、7、9（步长 2）
seq 1 2 10
# 生成 01 到 10
seq -w 1 10
```

### time

统计命令执行耗时

**示例：**

```bash
# 查看打包耗时
time tar -czf b.tar.gz bigdir/
# 查看脚本执行时间
time ./script.sh
```

### clear

清空终端屏幕（快捷键 Ctrl+L）

**示例：**

```bash
# 清屏后提示符回到顶部
clear
```

### type

判断命令类型：内置命令、别名、外部程序

**示例：**

```bash
# 输出 cd is a shell builtin（内置命令）
type cd
# 输出 ls 是外部程序及其路径
type ls
```

### jobs 控制

终端快捷键与作业控制组合

**常用选项：**

| 选项 | 说明 |
| --- | --- |
| `Ctrl+C` | 中断当前前台命令 |
| `Ctrl+D` | 退出当前 shell / 输入 EOF |
| `Ctrl+R` | 反向搜索命令历史 |
| `Ctrl+Z` | 挂起当前任务到后台 |
| `!!` | 重复上一条命令 |
| `!$` | 引用上一条命令的最后一个参数 |

**示例：**

```bash
# 输入关键字反向搜索历史命令，回车执行
Ctrl+R
# 创建目录并立即进入它
mkdir /tmp/x && cd !$
# 用 sudo 重跑上一条失败的命令
sudo !!
```

---

> 共收录 107 条常用命令，覆盖 10 个分类。

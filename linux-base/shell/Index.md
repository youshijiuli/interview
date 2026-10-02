# Index

## 集群分发

> 需求：循环复制文件到所有节点的相同目录下
> 
> 

```Bash
#!/bin/bash
 
#1. 判断参数个数
**if** [ $# -lt 1 ]
**then**
  echo Not Enough Arguement!
  exit;
**fi**
 
#2. 遍历集群所有机器
**for** host **in** hadoop102 hadoop103 hadoop104
**do**
  echo ====================  $host  ====================
  #3. 遍历所有目录，挨个发送
  **for** file **in** $@
  **do**
    #4 判断文件是否存在
    **if** [ -e $file ]
    **then**
      #5. 获取父目录
      pdir=$(cd -P $(dirname $file); pwd)
      #6. 获取当前文件的名称
      fname=$(basename $file)
      ssh $host "mkdir -p $pdir"
      rsync -av $pdir/$fname $host:$pdir
    **else**
      echo $file does not exists!
    **fi**
  **done**
**done**
```



## xcall

比如说在所有节点执行相同的命令，此时就需要一个一个机器去执行，极其少还好买多了就比较麻烦，所以执行明明就是用此脚本

> xcall command 
> 
> 

```Bash
#! /bin/bash
 
**for** i **in** hadoop102 hadoop103 hadoop104
**do**
    echo --------- $i ----------
    ssh $i "$*"
**done**
```



**Shell概述**

**Linux提供的Shell解析器有**

```Bash
[atguigu@hadoop101 ~]$ cat /etc/shells 
/bin/sh
/bin/bash
/sbin/nologin
/usr/bin/sh
/usr/bin/bash
/usr/sbin/nologin
/bin/tcsh
/bin/csh
```

- **bash和sh的关系**

```Bash
[atguigu@hadoop101 bin]$ ll | grep bash
-rwxr-xr-x. 1 root root 941880 5月  11 2016 bash
lrwxrwxrwx. 1 root root      4 5月  27 2017 sh -> bash
```

- **Centos默认的解析器是bash**

```Bash
[atguigu@hadoop101 bin]$ echo $SHELL
/bin/bash
```



**Shell脚本入门**

- **脚本格式**

脚本以\#\!/bin/bash开头（指定解析器）。

**第一个Shell脚本：helloworld.sh**

- 需求：创建一个Shell脚本，输出helloworld。

- 案例实操：

```Bash
[atguigu@hadoop101 shells]$ touch helloworld.sh
[atguigu@hadoop101 shells]$ vim helloworld.sh
```



在helloworld.sh中输入如下内容

```Bash
#!/bin/bash
echo "helloworld"
```

- 脚本的常用执行方式。

第一种：采用bash或sh\+脚本的相对路径或绝对路径（不用赋予脚本\+x权限）。

sh\+脚本的相对路径。

[atguigu@hadoop101 shells]$ sh ./helloworld.sh 

Helloworld

sh\+脚本的绝对路径。

[atguigu@hadoop101 shells]$ sh /home/atguigu/shells/helloworld.sh 

helloworld

bash\+脚本的相对路径。

[atguigu@hadoop101 shells]$ bash ./helloworld.sh 

Helloworld

bash\+脚本的绝对路径。

[atguigu@hadoop101 shells]$ bash /home/atguigu/shells/helloworld.sh 

Helloworld

第二种：采用输入脚本的绝对路径或相对路径执行脚本（必须具有可执行权限\+x）。

① 首先要赋予helloworld.sh 脚本的\+x权限。

[atguigu@hadoop101 shells]$ chmod \+x helloworld.sh

② 执行脚本。

相对路径。

[atguigu@hadoop101 shells]$ ./helloworld.sh

Helloworld

绝对路径。

[atguigu@hadoop101 shells]$ /home/atguigu/shells/helloworld.sh 

Helloworld

注意：第一种执行方法，本质是bash解析器帮你执行脚本，所以脚本本身不需要执行权限。第二种执行方法，本质是脚本需要自己执行，所以需要执行权限。









## 基础知识

### 注释

注释可以说明你的代码是什么作用，以及为什么这样写。

shell 语法中，注释是特殊的语句，会被 shell 解释器忽略。

- 单行注释 - 以 `#` 开头，到行尾结束。

- 多行注释 - 以 `:<<EOF` 开头，到 `EOF` 结束。

**💻 『示例源码』**

```Bash
#--------------------------------------------
shell 注释示例
author：zp
#--------------------------------------------

echo '这是单行注释'

########## 这是分割线 ##########

:<<EOF
echo '这是多行注释'
echo '这是多行注释'
echo '这是多行注释'
EOF
```

### echo

echo 用于字符串的输出。

输出普通字符串：

```Shell
echo "hello, world"
Output: hello, world
```

输出含变量的字符串：

```Shell
echo "hello, \"zp\""
Output: hello, "zp"
```

输出含变量的字符串：

```Shell
name=zp
echo "hello, \"${name}\""
Output: hello, "zp"
```

输出含换行符的字符串：

```Shell
# 输出含换行符的字符串
echo "YES\nNO"
Output: YES\nNO

echo -e "YES\nNO" # -e 开启转义
Output:
YES
NO
```

输出含不换行符的字符串：

```Bash
echo "YES"
echo "NO"
Output:
YES
NO

echo -e "YES\c" # -e 开启转义 \c 不换行
echo "NO"
Output:
YESNO
```

输出重定向至文件

```Shell
echo "test" > test.txt
输出执行结果
echo pwd
Output:(当前目录路径)
```

**💻 『示例源码』**

```Shell
#!/usr/bin/env bash

# 输出普通字符串
echo "hello, world"
#  Output: hello, world

# 输出含变量的字符串
echo "hello, \"zp\""
#  Output: hello, "zp"

# 输出含变量的字符串
name=zp
echo "hello, \"${name}\""
#  Output: hello, "zp"

# 输出含换行符的字符串
echo "YES\nNO"
#  Output: YES\nNO
echo -e "YES\nNO" # -e 开启转义
#  Output:
#  YES
#  NO

# 输出含不换行符的字符串
echo "YES"
echo "NO"
#  Output:
#  YES
#  NO

echo -e "YES\c" # -e 开启转义 \c 不换行
echo "NO"
#  Output:
#  YESNO

# 输出内容定向至文件
echo "test" > test.txt

# 输出执行结果
echo `pwd`
#  Output:(当前目录路径)

```

### printf

printf 用于格式化输出字符串。

默认，printf 不会像 echo 一样自动添加换行符，如果需要换行可以手动添加 `\n`。

**💻 『示例源码』**

```Shell
# 单引号
printf '%d %s\n' 1 "abc"
#  Output:1 abc

# 双引号
printf "%d %s\n" 1 "abc"
#  Output:1 abc

# 无引号
printf %s abcdef
#  Output: abcdef(并不会换行)

# 格式只指定了一个参数，但多出的参数仍然会按照该格式输出
printf "%s\n" abc def
#  Output:
#  abc
#  def

printf "%s %s %s\n" a b c d e f g h i j
#  Output:
#  a b c
#  d e f
#  g h i
#  j

# 如果没有参数，那么 %s 用 NULL 代替，%d 用 0 代替
printf "%s and %d \n"
#  Output:
#   and 0

# 格式化输出
printf "%-10s %-8s %-4s\n" 姓名 性别 体重kg
printf "%-10s %-8s %-4.2f\n" 郭靖 男 66.1234
printf "%-10s %-8s %-4.2f\n" 杨过 男 48.6543
printf "%-10s %-8s %-4.2f\n" 郭芙 女 47.9876
#  Output:
#  姓名     性别   体重kg
#  郭靖     男      66.12
#  杨过     男      48.65
#  郭芙     女      47.99
```

printf 的转义符



































## **变量**

1. **系统预定义变量**

    - **常用系统变量**

$HOME、$PWD、$SHELL、$USER等

- **案例实操**

    - 查看系统变量的值。

[atguigu@hadoop101 shells]$ echo $HOME

/home/atguigu

- 显示当前Shell中所有变量：set。

[atguigu@hadoop101 shells]$ set

BASH=/bin/bash

BASH_ALIASES=()

BASH_ARGC=()

BASH_ARGV=()

**自定义变量**

- **基本语法**

    - 定义变量：变量名=变量值，注意，=号前后不能有空格。

    - 撤销变量：unset 变量名。

    - 声明静态变量：readonly变量，注意：不能unset。

- **变量定义规则**

    - 变量名称可以由字母、数字和下划线组成，但是不能以数字开头，环境变量名建议大写。

    - 等号两侧不能有空格。

    - 在bash中，变量默认类型都是字符串类型，无法直接进行数值运算。

    - 变量的值如果有空格，需要使用双引号或单引号括起来。

- **案例实操**

    - 定义变量A。

[atguigu@hadoop101 shells]$ A=5

[atguigu@hadoop101 shells]$ echo $A

5

- 给变量A重新赋值。

[atguigu@hadoop101 shells]$ A=8

[atguigu@hadoop101 shells]$ echo $A

8

- 撤销变量A。

[atguigu@hadoop101 shells]$ unset A

[atguigu@hadoop101 shells]$ echo $A

- 声明静态的变量B=2，不能unset。

[atguigu@hadoop101 shells]$ readonly B=2

[atguigu@hadoop101 shells]$ echo $B

2

[atguigu@hadoop101 shells]$ B=9

-bash: B: readonly variable

- 在bash中，变量默认类型都是字符串类型，无法直接进行数值运算。

[atguigu@hadoop102 \~]$ C=1\+2

[atguigu@hadoop102 \~]$ echo $C

1\+2

- 变量的值如果有空格，需要使用双引号或单引号括起来。

[atguigu@hadoop102 \~]$ D=I love banzhang

-bash: world: command not found

[atguigu@hadoop102 \~]$ D="I love banzhang"

[atguigu@hadoop102 \~]$ echo $D

I love banzhang

- 可把变量提升为全局环境变量，可供其他Shell程序使用。

export 变量名

[atguigu@hadoop101 shells]$ vim helloworld.sh 

在helloworld.sh文件中增加echo $B。

\#\!/bin/bash



echo "helloworld"

echo $B



[atguigu@hadoop101 shells]$ ./helloworld.sh 

Helloworld

发现并没有打印输出变量B的值。

[atguigu@hadoop101 shells]$ export B

[atguigu@hadoop101 shells]$ ./helloworld.sh 

helloworld

2



## **特殊变量**

1. **$n**

    - **基本语法**

$n （功能描述：n为数字，$0代表该脚本名称，$1-$9代表第一到第九个参数，十以上的参数需要用大括号包含，如$\{10\}。）

- **案例实操**

[atguigu@hadoop101 shells]$ touch parameter.sh 

[atguigu@hadoop101 shells]$ vim parameter.sh

\#\!/bin/bash

echo '==========$n=========='

echo $0 

echo $1 

echo $2



[atguigu@hadoop101 shells]$ chmod 777 parameter.sh

[atguigu@hadoop101 shells]$ ./parameter.sh cls xz

==========$n==========

./parameter.sh

cls

xz

1. **$\#**

    - **基本语法**

$\# （功能描述：获取所有输入参数个数，常用于循环，判断参数的个数是否正确以及加强脚本的健壮性）。

- **案例实操**

[atguigu@hadoop101 shells]$ vim parameter.sh

\#\!/bin/bash

echo '==========$n=========='

echo $0 

echo $1 

echo $2

echo '==========$\#=========='

echo $\#



[atguigu@hadoop101 shells]$ chmod 777 parameter.sh

[atguigu@hadoop101 shells]$ ./parameter.sh cls xz

==========$n==========

./parameter.sh

cls

xz

==========$\#==========

2

2. **$*、$@**

    - **基本语法**

$* （功能描述：这个变量代表命令行中所有的参数，$*把所有的参数看成一个整体）

$@ （功能描述：这个变量也代表命令行中所有的参数，不过$@把每个参数区分对待）

- **案例实操**

[atguigu@hadoop101 shells]$ vim parameter.sh

\#\!/bin/bash

echo '==========$n=========='

echo $0 

echo $1 

echo $2

echo '==========$\#=========='

echo $\#

echo '==========$*=========='

echo $*

echo '==========$@=========='

echo $@

[atguigu@hadoop101 shells]$ ./parameter.sh a b c d e f g

==========$n==========

./parameter.sh

a

b

==========$\#==========

7

==========$*==========

a b c d e f g

==========$@==========

a b c d e f g

3. **$？**

    - **基本语法**

$？ （功能描述：最后一次执行的命令的返回状态。如果这个变量的值为0，证明上一个命令正确执行；如果这个变量的值为非0（具体是哪个数，由命令自己来决定），则证明上一个命令执行不正确了）

- **案例实操**

判断helloworld.sh脚本是否正确执行。

[atguigu@hadoop101 shells]$ ./helloworld.sh 

hello world

[atguigu@hadoop101 shells]$ echo $?

0





- `$#` 参数个数

- `$*` 显示所有参数,以"$1 $2 … $n"的形式输出所有参数

- `$@` 显示所有参数,以"$1" "$2" … "$n" 的形式输出所有参数

- `$$` 脚本运行的当前进程ID号

- `$!` 后台运行的最后一个进程的ID号

- `$?` 显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。



```Bash
#!/bin/bash
echo "-- \$* 演示 ---"
for i in "$*"; do
    echo $i
done

echo "-- \$@ 演示 ---"
for i in "$@"; do
    echo $i
done
#输出
$ ./test.sh 1 2 3
-- $* 演示 ---
1 2 3
-- $@ 演示 ---
1
2
3
```







**变量**

跟许多程序设计语言一样，你可以在 bash 中创建变量。

Bash 中没有数据类型，bash 中的变量可以保存一个数字、一个字符、一个字符串等等。同时无需提前声明变量，给变量赋值会直接创建变量。

变量命名原则

- 命名只能使用英文字母，数字和下划线，首个字符不能以数字开头。

- 中间不能有空格，可以使用下划线（_）。

- 不能使用标点符号。

- 不能使用 bash 里的关键字（可用 help 命令查看保留关键字）。

声明变量

访问变量的语法形式为：`${var}` 和 `$var` 。

变量名外面的花括号是可选的，加不加都行，加花括号是为了帮助解释器识别变量的边界，所以推荐加花括号。

```Shell
word="hello"
echo ${word}
Output: hello
```

只读变量

使用 readonly 命令可以将变量定义为只读变量，只读变量的值不能被改变。

```Bash
rword="hello"
echo ${rword}
readonly rword
rword="bye"  # 如果放开注释，执行时会报错
```

删除变量

使用 unset 命令可以删除变量。变量被删除后不能再次使用。unset 命令不能删除只读变量。

```Bash
dword="hello"  # 声明变量
echo ${dword}  # 输出变量值
Output: hello

unset dword    # 删除变量
echo ${dword}
Output: （空）
```

变量类型

- **局部变量** - 局部变量是仅在某个脚本内部有效的变量。它们不能被其他的程序和脚本访问。

- **环境变量** - 环境变量是对当前 shell 会话内所有的程序或脚本都可见的变量。创建它们跟创建局部变量类似，但使用的是 `export` 关键字，shell 脚本也可以定义环境变量。

常见的环境变量：

[这里](http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_03_02.html###sect_03_02_04) 有一张更全面的 Bash 环境变量列表。

**💻 『示例源码』**

```Bash
#!/usr/bin/env bash

################### 声明变量 ###################
name="world"
echo "hello ${name}"
# Output: hello world

################### 输出变量 ###################
folder=$(pwd)
echo "current path: ${folder}"

################### 只读变量 ###################
rword="hello"
echo ${rword}
# Output: hello
readonly rword
# rword="bye"  # 如果放开注释，执行时会报错

################### 删除变量 ###################
dword="hello" # 声明变量
echo ${dword} # 输出变量值
# Output: hello

unset dword # 删除变量
echo ${dword}
# Output: （空）

################### 系统变量 ###################
echo "UID:$UID"
echo LOGNAME:$LOGNAME
echo User:$USER
echo HOME:$HOME
echo PATH:$PATH
echo HOSTNAME:$HOSTNAME
echo SHELL:$SHELL
echo LANG:$LANG

################### 自定义变量 ###################
days=10
user="admin"
echo "$user logged in $days days age"
days=5
user="root"
echo "$user logged in $days days age"
# Output:
# admin logged in 10 days age
# root logged in 5 days age

################### 从变量读取列表 ###################
colors="Red Yellow Blue"
colors=$colors" White Black"

for color in $colors
do
        echo " $color"
done
```















## **运算符**

- **基本语法**

“$((运算式))” 或 “$[运算式]”

- **案例实操： **

计算（2\+3）* 4的值

[atguigu@hadoop101 shells]\# S=$[(2\+3)*4]

[atguigu@hadoop101 shells]\# echo $S

- **条件判断**

    - **基本语法**

        - test condition

        - [ condition ]（注意condition前后要有空格）

注意：条件非空即为true，[ atguigu ]返回true，[  ] 返回false。

- **常用判断条件**

    - 两个整数之间比较

- -eq 等于（equal）

- -ne 不等于（not equal）

- -lt 小于（less than）

- -le 小于等于（less equal）

- -gt 大于（greater than）

- -ge 大于等于（greater equal） 

    - 按照文件权限进行判断

- -r 有读的权限（read） 

- -w 有写的权限（write）

- -x 有执行的权限（execute）

    - 按照文件类型进行判断

- -e 文件存在（existence）

- -f 文件存在并且是一个常规的文件（file）

- -d 文件存在并且是一个目录（directory）

    - **案例实操**

        - 23是否大于等于22。

[atguigu@hadoop101 shells]$ [ 23 -ge 22 ]

[atguigu@hadoop101 shells]$ echo $?

0

- helloworld.sh是否具有写权限。

[atguigu@hadoop101 shells]$ [ -w helloworld.sh ]

[atguigu@hadoop101 shells]$ echo $?

0

- /home/atguigu/cls.txt目录中的文件是否存在。

[atguigu@hadoop101 shells]$ [ -e /home/atguigu/cls.txt ]

[atguigu@hadoop101 shells]$ echo $?

1

- 多条件判断（\&\& 表示前一条命令执行成功时，才执行后一条命令，\|\| 表示上一条命令执行失败后，才执行下一条命令）。

[atguigu@hadoop101 \~]$ [ atguigu ] \&\& echo OK \|\| echo notOK

OK

[atguigu@hadoop101 shells]$ [ ] \&\& echo OK \|\| echo notOK

notOK







## 运算符

### 算数运算符

下表列出了常用的算术运算符，假定变量 x 为 10，变量 y 为 20：

**注意：**条件表达式要放在方括号之间，并且要有空格，例如: `[$x==$y]` 是错误的，必须写成 `[ $x == $y ]`。

**💻 『示例源码』**

```Bash
x=10
y=20

echo "x=${x}, y=${y}"

val=`expr ${x} + ${y}`
echo "${x} + ${y} = $val"

val=`expr ${x} - ${y}`
echo "${x} - ${y} = $val"

val=`expr ${x} * ${y}`
echo "${x} * ${y} = $val"

val=`expr ${y} / ${x}`
echo "${y} / ${x} = $val"

val=`expr ${y} % ${x}`
echo "${y} % ${x} = $val"

if [[ ${x} == ${y} ]]
then
  echo "${x} = ${y}"
fi
if [[ ${x} != ${y} ]]
then
  echo "${x} != ${y}"
fi

#  Output:
#  x=10, y=20
#  10 + 20 = 30
#  10 - 20 = -10
#  10 * 20 = 200
#  20 / 10 = 2
#  20 % 10 = 0
#  10 != 20
```



```Shell
#!/bin/bash

a=10
b=20

val=expr $a + $b
echo "a + b : $val" #a + b : 30
val=expr $a - $b
echo "a - b : $val" #a - b : -10
val=expr $a * $b
echo "a * b : $val" #a * b : 200
val=expr $b / $a
echo "b / a : $val" #b / a : 2
val=expr $b % $a
echo "b % a : $val" #b % a : 0
```



### 关系运算符

- `-eq`：相等

- `-ne`：不相等

- `-gt`：大于

- `-lt`：小于

- `-ge`：大于等于

- `-le`：小于等于

关系运算符只支持数字，不支持字符串，除非字符串的值是数字。

下表列出了常用的关系运算符，假定变量 x 为 10，变量 y 为 20：

**💻 『示例源码』**

```Bash
x=10
y=20

echo "x=${x}, y=${y}"

if [[ ${x} -eq ${y} ]]; then
   echo "${x} -eq ${y} : x 等于 y"
else
   echo "${x} -eq ${y}: x 不等于 y"
fi

if [[ ${x} -ne ${y} ]]; then
   echo "${x} -ne ${y}: x 不等于 y"
else
   echo "${x} -ne ${y}: x 等于 y"
fi

if [[ ${x} -gt ${y} ]]; then
   echo "${x} -gt ${y}: x 大于 y"
else
   echo "${x} -gt ${y}: x 不大于 y"
fi

if [[ ${x} -lt ${y} ]]; then
   echo "${x} -lt ${y}: x 小于 y"
else
   echo "${x} -lt ${y}: x 不小于 y"
fi

if [[ ${x} -ge ${y} ]]; then
   echo "${x} -ge ${y}: x 大于或等于 y"
else
   echo "${x} -ge ${y}: x 小于 y"
fi

if [[ ${x} -le ${y} ]]; then
   echo "${x} -le ${y}: x 小于或等于 y"
else
   echo "${x} -le ${y}: x 大于 y"
fi

#  Output:
#  x=10, y=20
#  10 -eq 20: x 不等于 y
#  10 -ne 20: x 不等于 y
#  10 -gt 20: x 不大于 y
#  10 -lt 20: x 小于 y
#  10 -ge 20: x 小于 y
#  10 -le 20: x 小于或等于 y
```

```Bash
#!/bin/bash

a=10
b=20
if [ $a -eq $b ]
then
   echo "$a -eq $b : a 等于 b"
else
   echo "$a -eq $b: a 不等于 b"
fi
```



### 布尔运算符

- `!`：非，`[ ! false ]`：true

- `-o`：或运算，`[ $a -lt 20 -o $b -gt 100 ]`：a小于20 或 b大于100

- `-a`：与运算，`[ $a -lt 20 -a $b -gt 100 ]`：a小于20 且 b大于100

下表列出了常用的布尔运算符，假定变量 x 为 10，变量 y 为 20：

**💻 『示例源码』**

```Bash
x=10
y=20

echo "x=${x}, y=${y}"

if [[ ${x} != ${y} ]]; then
   echo "${x} != ${y} : x 不等于 y"
else
   echo "${x} != ${y}: x 等于 y"
fi

if [[ ${x} -lt 100 && ${y} -gt 15 ]]; then
   echo "${x} 小于 100 且 ${y} 大于 15 : 返回 true"
else
   echo "${x} 小于 100 且 ${y} 大于 15 : 返回 false"
fi

if [[ ${x} -lt 100 || ${y} -gt 100 ]]; then
   echo "${x} 小于 100 或 ${y} 大于 100 : 返回 true"
else
   echo "${x} 小于 100 或 ${y} 大于 100 : 返回 false"
fi

if [[ ${x} -lt 5 || ${y} -gt 100 ]]; then
   echo "${x} 小于 5 或 ${y} 大于 100 : 返回 true"
else
   echo "${x} 小于 5 或 ${y} 大于 100 : 返回 false"
fi

#  Output:
#  x=10, y=20
#  10 != 20 : x 不等于 y
#  10 小于 100 且 20 大于 15 : 返回 true
#  10 小于 100 或 20 大于 100 : 返回 true
#  10 小于 5 或 20 大于 100 : 返回 false
```







### 逻辑运算符

- `&&`：逻辑and

- `||`：逻辑or

以下介绍 Shell 的逻辑运算符，假定变量 x 为 10，变量 y 为 20:

**💻 『示例源码』**

```Bash
x=10
y=20

echo "x=${x}, y=${y}"

if [[ ${x} -lt 100 && ${y} -gt 100 ]]
then
   echo "${x} -lt 100 && ${y} -gt 100 返回 true"
else
   echo "${x} -lt 100 && ${y} -gt 100 返回 false"
fi

if [[ ${x} -lt 100 || ${y} -gt 100 ]]
then
   echo "${x} -lt 100 || ${y} -gt 100 返回 true"
else
   echo "${x} -lt 100 || ${y} -gt 100 返回 false"
fi

#  Output:
#  x=10, y=20
#  10 -lt 100 && 20 -gt 100 返回 false
#  10 -lt 100 || 20 -gt 100 返回 true
```



```Bash
#!/bin/bash

a=10
b=20

if [[ $a -lt 100 && $b -gt 100 ]]
then
   echo "返回 true"
else
   echo "返回 false"  #a小于100 且 b大于100
fi

if [[ $a -lt 100 || $b -gt 100 ]]
then
   echo "返回 true" #a小于100 且 b大于100
else
   echo "返回 false"
fi
```

































## **流程控制（重点）**

跟其它程序设计语言一样，Bash 中的条件语句让我们可以决定一个操作是否被执行。结果取决于一个包在`[[ ]]`里的表达式。

由`[[ ]]`（`sh`中是`[ ]`）包起来的表达式被称作 **检测命令** 或 **基元**。这些表达式帮助我们检测一个条件的结果。这里可以找到有关[bash 中单双中括号区别](http://serverfault.com/a/52050)的答案。

共有两个不同的条件表达式：`if`和`case`。

### **if判断**



- 单分支

    ```Shell
    if [ 条件判断式 ];then 
        程序 
    fi 
    或者 
    if  [ 条件判断式 ] 
    then
        程序 
    fi
    ```

- 多分支

    ```Shell
    if [ 条件判断式 ] 
    then
        程序 
    elif [ 条件判断式 ]
    then
     程序
    else
     程序
    fi
    ```

注意事项：

① [ 条件判断式 ]，中括号和条件判断式之间必须有空格

② if后要有空格

- **案例实操**

输入一个数字，如果是1，则输出banzhang zhen shuai，如果是2，则输出cls zhen mei，如果是其它，什么也不输出。

[atguigu@hadoop101 shells]$ touch if.sh

[atguigu@hadoop101 shells]$ vim if.sh



\#\!/bin/bash



if [ $1 -eq 1 ]

then

echo "banzhang zhen shuai"

elif [ $1 -eq 2 ]

then

echo "cls zhen mei"

fi



[atguigu@hadoop101 shells]$ chmod 777 if.sh 

[atguigu@hadoop101 shells]$ ./if.sh 1

banzhang zhen shuai





（1）`if` 语句

`if`在使用上跟其它语言相同。如果中括号里的表达式为真，那么`then`和`fi`之间的代码会被执行。`fi`标志着条件代码块的结束。

```Shell
写成一行
if [[ 1 -eq 1 ]]; then echo "1 -eq 1 result is: true"; fi
Output: 1 -eq 1 result is: true

写成多行
if [[ "abc" -eq "abc" ]]
then
  echo ""abc" -eq "abc" result is: true"
fi
Output: abc -eq abc result is: true

```



（2）if else 语句
同样，我们可以使用if..else语句，例如：

```Bash
if [[ 2 -ne 1 ]]; then
  echo "true"
else
  echo "false"
fi
Output: true
```





（3）`if elif else` 语句

有些时候，`if..else`不能满足我们的要求。别忘了`if..elif..else`，使用起来也很方便。

**💻 『示例源码』**

```Shell
x=10
y=20
if [[ ${x} > ${y} ]]; then
   echo "${x} > ${y}"
elif [[ ${x} < ${y} ]]; then
   echo "${x} < ${y}"
else
   echo "${x} = ${y}"
fi
# Output: 10 < 20
```

```Bash
#!/bin/bash
read -p "请输入您的分数:" SCORE

if [ $SCORE -ge 90 ];then
        echo "优秀"
    elif [ $SCORE -ge 80 ];then
        echo "良好"
    elif [ $SCORE -ge 70 ];then
        echo "不错"
    elif [ $SCORE -ge 60 ];then
        echo "合格"
    else
        echo "差劲"
fi
```





### **case语句**

如果你需要面对很多情况，分别要采取不同的措施，那么使用`case`会比嵌套的`if`更有用。使用`case`来解决复杂的条件判断，看起来像下面这样：

```Shell
case $变量名 in 
"值1"）
    如果变量的值等于值1，则执行程序1 
;; 
"值2"）
    如果变量的值等于值2，则执行程序2 
;;
    …省略其他分支… 
*）
    如果变量的值都不是以上的值，则执行此程序 
;; 
esac
```

注意事项：

（1）case行尾必须为单词“in”，每一个模式匹配必须以右括号“）”结束。

（2）双分号“;;”表示命令序列结束，相当于java中的break。

（3）最后的“*）”表示默认模式，相当于java中的default。

每种情况都是匹配了某个模式的表达式。`|`用来分割多个模式，`)`用来结束一个模式序列。第一个匹配上的模式对应的命令将会被执行。`*`代表任何不匹配以上给定模式的模式。命令块儿之间要用`;;`分隔。

- **案例实操**

输入一个数字，如果是1，则输出banzhang，如果是2，则输出cls，如果是其它，输出renyao。

```Shell
[atguigu@hadoop101 shells]$ touch case.sh
[atguigu@hadoop101 shells]$ vim case.sh
```



```Bash
!/bin/bash
 
case $1 in
"1")
        echo "banzhang"
;;
 
"2")
        echo "cls"
;;
*)
        echo "renyao"
;;
esac
```



```Shell
[atguigu@hadoop101 shells]$ chmod 777 case.sh
[atguigu@hadoop101 shells]$ ./case.sh 1
1
```



```Bash
#!/bin/bash
if [ $(ps -ef | grep -c "ssh") -gt 1 ]; then echo "true"; fi

num1=$[2*3]
num2=$[1+5]
if test $[num1] -eq $[num2]
then
    echo '两个数字相等!'  #
else
    echo '两个数字不相等!'
fi
```

```Bash
exec
case ${oper} in
  "+")
    val=`expr ${x} + ${y}`
    echo "${x} + ${y} = ${val}"
  ;;
  "-")
    val=`expr ${x} - ${y}`
    echo "${x} - ${y} = ${val}"
  ;;
  "*")
    val=`expr ${x} * ${y}`
    echo "${x} * ${y} = ${val}"
  ;;
  "/")
    val=`expr ${x} / ${y}`
    echo "${x} / ${y} = ${val}"
  ;;
  *)
    echo "Unknown oper!"
  ;;
esac
```



```Bash
#!/bin/bash

item=1;

case "${item}" in
    1)
        echo "item = 1"
    ;;
    2|3)
        echo "item = 2 or item = 3"
    ;;
    *)
        echo "default (none of above)"
    ;;
esac
```



```Bash
#!/bin/bash

case $1 in
"1")
 echo "1111"
;;
"2")
 echo "222"
;;
"3")
 echo "333"
;;
*)
 echo "啥也不是...."
;;
esac
```



### 循环

循环其实不足为奇。跟其它程序设计语言一样，bash 中的循环也是只要控制条件为真就一直迭代执行的代码块。

Bash 中有四种循环：`for`，`while`，`until`和`select`。



















#### **for循环**

`for`与它在 C 语言中的姊妹非常像。看起来是这样：

```Shell
for arg in elem1 elem2 ... elemN
do
  ### 语句
done
```

在每次循环的过程中，`arg`依次被赋值为从`elem1`到`elemN`。这些值还可以是通配符或者[大括号扩展](https://github.com/denysdovhan/bash-handbook/blob/master/translations/zh-CN/README.md#%E5%A4%A7%E6%8B%AC%E5%8F%B7%E6%89%A9%E5%B1%95)。

当然，我们还可以把`for`循环写在一行，但这要求`do`之前要有一个分号，就像下面这样：

```Shell
for i in {1..5}; do echo $i; done
```

还有，如果你觉得`for..in..do`对你来说有点奇怪，那么你也可以像 C 语言那样使用`for`，比如：

```Shell
for (( i = 0; i < 10; i++ )); do
  echo $i
done
```

当我们想对一个目录下的所有文件做同样的操作时，`for`就很方便了。举个例子，如果我们想把所有的`.bash`文件移动到`script`文件夹中，并给它们可执行权限，我们的脚本可以这样写：

**💻 『示例源码』**

```Bash
DIR=/home/zp
for FILE in ${DIR}/*.sh; do
  mv "$FILE" "${DIR}/scripts"
done
# 将 /home/zp 目录下所有 sh 文件拷贝到 /home/zp/scripts
```





**基本语法1**

for (( 初始值;循环控制条件;变量变化 )) 

do 

程序 

done

- **案例实操**

从1加到100。

[atguigu@hadoop101 shells]$ touch for1.sh

[atguigu@hadoop101 shells]$ vim for1.sh



\#\!/bin/bash



sum=0

for((i=0;i\<=100;i\+\+))

do

sum=$[$sum\+$i]

done

echo $sum



[atguigu@hadoop101 shells]$ chmod 777 for1.sh 

[atguigu@hadoop101 shells]$ ./for1.sh 

5050

- **基本语法2**

for 变量 in 值1 值2 值3… 

do 

程序 

done

- **案例实操**

    - 打印所有输入参数。

[atguigu@hadoop101 shells]$ touch for2.sh

[atguigu@hadoop101 shells]$ vim for2.sh



\#\!/bin/bash

\#打印数字



for i in cls mly wls

do

echo "ban zhang love $i"

done



[atguigu@hadoop101 shells]$ chmod 777 for2.sh 

[atguigu@hadoop101 shells]$ ./for2.sh

ban zhang love cls

ban zhang love mly

ban zhang love wls

- 比较$*和$@区别。

$*和$@都表示传递给函数或脚本的所有参数，不被双引号“”包含时，都以$1 $2 …$n的形式输出所有参数。

[atguigu@hadoop101 shells]$ touch for3.sh

[atguigu@hadoop101 shells]$ vim for3.sh



\#\!/bin/bash 

echo '=============$*============='

for i in $*

do

echo "ban zhang love $i"

done



echo '=============$@============='

for j in $@

do       echo "ban zhang love $j"

done



[atguigu@hadoop101 shells]$ chmod 777 for3.sh

[atguigu@hadoop101 shells]$ ./for3.sh cls mly wls

=============$*=============

banzhang love cls

banzhang love mly

banzhang love wls

=============$@=============

banzhang love cls

banzhang love mly

banzhang love wls

当它们被双引号“”包含时，$*会将所有的参数作为一个整体，以“$1 $2 …$n”的形式输出所有参数；$@会将各个参数分开，以“$1” “$2”…“$n”的形式输出所有参数。

[atguigu@hadoop101 shells]$ vim for4.sh



\#\!/bin/bash 

echo '=============$*============='

for i in "$*" 

\#$*中的所有参数看成是一个整体，所以这个for循环只会循环一次 

do

echo "ban zhang love $i"

done 



echo '=============$@============='

for j in "$@" 

\#$@中的每个参数都看成是独立的，所以“$@”中有几个参数，就会循环几次 

do

echo "ban zhang love $j" 

done



[atguigu@hadoop101 shells]$ chmod 777 for4.sh

[atguigu@hadoop101 shells]$ ./for4.sh cls mly wls

=============$*=============

banzhang love cls mly wls

=============$@=============

banzhang love cls

banzhang love mly

banzhang love wls



```Bash
#!/bin/bash
for str in 'This is a string'
do
    echo $str
done
# 动态读取入参
for var in $@
do
    echo $var
done
```



#### **while循环**

`while`循环检测一个条件，只要这个条件为 *真*，就执行一段命令。被检测的条件跟`if..then`中使用的[基元](https://github.com/denysdovhan/bash-handbook/blob/master/translations/zh-CN/README.md#%E5%9F%BA%E5%85%83%E5%92%8C%E7%BB%84%E5%90%88%E8%A1%A8%E8%BE%BE%E5%BC%8F)并无二异。因此一个`while`循环看起来会是这样：

```Shell
while [[ condition ]]
do
  ### 语句
done
```

跟`for`循环一样，如果我们把`do`和被检测的条件写到一行，那么必须要在`do`之前加一个分号。



- **案例实操**

从1加到100。

[atguigu@hadoop101 shells]$ touch while.sh

[atguigu@hadoop101 shells]$ vim while.sh



\#\!/bin/bash

sum=0

i=1

while [ $i -le 100 ]

do

sum=$[$sum\+$i]
        i=$[$i\+1]

done



echo $sum



[atguigu@hadoop101 shells]$ chmod 777 while.sh 

[atguigu@hadoop101 shells]$ ./while.sh 

5050



**read读取控制台输入**

- **基本语法**

read  （选项）  （参数）

① 选项：

- -p：指定读取值时的提示符。

- -t：指定读取值时等待的时间（秒）如果-t不加表示一直等待。

② 参数

变量：指定读取值的变量名。

- **案例实操**

提示7秒内，读取控制台输入的名称。

[atguigu@hadoop101 shells]$ touch read.sh

[atguigu@hadoop101 shells]$ vim read.sh



\#\!/bin/bash



read -t 7 -p "Enter your name in 7 seconds :" NN

echo $NN



[atguigu@hadoop101 shells]$ ./read.sh 

Enter your name in 7 seconds : atguigu

atguigu







```Bash
#!/bin/bash
echo 'Hello World!'

count=3
echo $count
logpath='home/test/shell/shell-test.log'
url='https://www.test.com/blog/shell-test'
输出字符串长度
echo ${#logpath} ${#url}
注意条件前后空格
while [ $count -gt 0 ]
do
    echo $logpath `\n` $url
    count=expr $count - 1
    echo $count
done

echo 'end...'

```

```Bash
#!/bin/bash
logpath='home/test/shell/shell-test.log'

# 读取logpath文件
while read line
do
    echo $line
done < $logpath
```

```Shell
### 0到9之间每个数的平方
x=0
while [[ ${x} -lt 10 ]]; do
  echo $((x * x))
  x=$((x + 1))
done
#  Output:
#  0
#  1
#  4
#  9
#  16
#  25
#  36
#  49
#  64
#  81
```















#### `until`循环

`until`循环跟`while`循环正好相反。它跟`while`一样也需要检测一个测试条件，但不同的是，只要该条件为 *假* 就一直执行循环：

**💻 『示例源码』**

```Bash
x=0
until [[ ${x} -ge 5 ]]; do
  echo ${x}
  x=expr ${x} + 1
done
Output:
0
1
2
3
4
```

#### `select`循环

`select`循环帮助我们组织一个用户菜单。它的语法几乎跟`for`循环一致：

```Shell
select answer in elem1 elem2 ... elemN
do
  ### 语句
done
```

`select`会打印`elem1..elemN`以及它们的序列号到屏幕上，之后会提示用户输入。通常看到的是`$?`（`PS3`变量）。用户的选择结果会被保存到`answer`中。如果`answer`是一个在`1..N`之间的数字，那么`语句`会被执行，紧接着会进行下一次迭代 —— 如果不想这样的话我们可以使用`break`语句。

**💻 『示例源码』**

```Bash
#!/usr/bin/env bash

PS3="Choose the package manager: "
select ITEM in bower npm gem pip
do
echo -n "Enter the package name: " && read PACKAGE
case ${ITEM} in
  bower) bower install ${PACKAGE} ;;
  npm) npm install ${PACKAGE} ;;
  gem) gem install ${PACKAGE} ;;
  pip) pip install ${PACKAGE} ;;
esac
break # 避免无限循环
done
```

这个例子，先询问用户他想使用什么包管理器。接着，又询问了想安装什么包，最后执行安装操作。

运行这个脚本，会得到如下输出：

```Shell
$ ./my_script
bower
npm
gem
pip
Choose the package manager: 2
Enter the package name: gitbook-cli
```

#### `break` 和 `continue`

如果想提前结束一个循环或跳过某次循环执行，可以使用 shell 的`break`和`continue`语句来实现。它们可以在任何循环中使用。

> `break`语句用来提前结束当前循环。
> 
> `continue`语句用来跳过某次迭代。
> 
> 

**💻 『示例源码』**

```Bash
查找 10 以内第一个能整除 2 和 3 的正整数
i=1
while [[ ${i} -lt 10 ]]; do
  if [[ $((i % 3)) -eq 0 ]] && [[ $((i % 2)) -eq 0 ]]; then
    echo ${i}
    break;
  fi
  i=expr ${i} + 1
done
Output: 6
```

**💻 『示例源码』**

```Bash
# 打印10以内的奇数
for (( i = 0; i < 10; i ++ )); do
  if [[ $((i % 2)) -eq 0 ]]; then
    continue;
  fi
  echo ${i}
done
Output:
1
3
5
7
9
```















## 数据类型





### 字符串

### 单引号和双引号

shell 字符串可以用单引号 `''`，也可以用双引号 `“”`，也可以不用引号。

- 单引号的特点

    - 单引号里不识别变量

    - 单引号里不能出现单独的单引号（使用转义符也不行），但可成对出现，作为字符串拼接使用。

- 双引号的特点

    - 双引号里识别变量

    - 双引号里可以出现转义字符

综上，推荐使用双引号。

拼接字符串

```Bash
# 使用单引号拼接
name1='white'
str1='hello, '${name1}''
str2='hello, ${name1}'
echo ${str1}_${str2}
Output:
hello, white_hello, ${name1}

# 使用双引号拼接
name2="black"
str3="hello, "${name2}""
str4="hello, ${name2}"
echo ${str3}_${str4}
Output:
hello, black_hello, black
```

获取字符串长度

```Shell
text="12345"
echo ${#text}
Output:
5
```

截取子字符串

```Shell
text="12345"
echo ${text:2:2}
Output:
34
```

从第 3 个字符开始，截取 2 个字符

查找子字符串

```Bash
#!/usr/bin/env bash

text="hello"
echo expr index "${text}" ll

Execute: ./str-demo5.sh
Output:
3
```

查找 `ll` 子字符在 `hello` 字符串中的起始位置。

**💻 『示例源码』**

```Bash
#!/usr/bin/env bash

################### 使用单引号拼接字符串 ###################
name1='white'
str1='hello, '${name1}''
str2='hello, ${name1}'
echo ${str1}_${str2}
# Output:
# hello, white_hello, ${name1}

################### 使用双引号拼接字符串 ###################
name2="black"
str3="hello, "${name2}""
str4="hello, ${name2}"
echo ${str3}_${str4}
# Output:
# hello, black_hello, black

################### 获取字符串长度 ###################
text="12345"
echo "${text} length is: ${#text}"
# Output:
# 12345 length is: 5

# 获取子字符串
text="12345"
echo ${text:2:2}
# Output:
# 34

################### 查找子字符串 ###################
text="hello"
echo `expr index "${text}" ll`
# Output:
# 3

################### 判断字符串中是否包含子字符串 ###################
result=$(echo "${str}" | grep "feature/")
if [[ "$result" != "" ]]; then
        echo "feature/ 是 ${str} 的子字符串"
else
        echo "feature/ 不是 ${str} 的子字符串"
fi

################### 截取关键字左边内容 ###################
full_branch="feature/1.0.0"
branch=`echo ${full_branch#feature/}`
echo "branch is ${branch}"

################### 截取关键字右边内容 ###################
full_version="0.0.1-SNAPSHOT"
version=`echo ${full_version%-SNAPSHOT}`
echo "version is ${version}"

################### 字符串分割成数组 ###################
str="0.0.0.1"
OLD_IFS="$IFS"
IFS="."
array=( ${str} )
IFS="$OLD_IFS"
size=${#array[*]}
lastIndex=`expr ${size} - 1`
echo "数组长度：${size}"
echo "最后一个数组元素：${array[${lastIndex}]}"
for item in ${array[@]}
do
        echo "$item"
done

################### 判断字符串是否为空 ###################
#-n 判断长度是否非零
#-z 判断长度是否为零

str=testing
str2=''
if [[ -n "$str" ]]
then
        echo "The string $str is not empty"
else
        echo "The string $str is empty"
fi

if [[ -n "$str2" ]]
then
        echo "The string $str2 is not empty"
else
        echo "The string $str2 is empty"
fi

#        Output:
#        The string testing is not empty
#        The string  is empty

################### 字符串比较 ###################
str=hello
str2=world
if [[ $str = "hello" ]]; then
        echo "str equals hello"
else
        echo "str not equals hello"
fi

if [[ $str2 = "hello" ]]; then
        echo "str2 equals hello"
else
        echo "str2 not equals hello"
fi
```



### 字符串运算符

- `[ $a = $b ]` 两个字符串是否相等

- `[ $a != $b ]` 两个字符串是否不相等

- `[ -z $a ]` 字符串长度是否为0

- `[ -n "$a" ]` 字符串长度是否不为 0

- `[ $a ]` 字符串是否为空

下表列出了常用的字符串运算符，假定变量 a 为 "abc"，变量 b 为 "efg"：

**💻 『示例源码』**

```Bash
x="abc"
y="xyz"


echo "x=${x}, y=${y}"

if [[ ${x} = ${y} ]]; then
   echo "${x} = ${y} : x 等于 y"
else
   echo "${x} = ${y}: x 不等于 y"
fi

if [[ ${x} != ${y} ]]; then
   echo "${x} != ${y} : x 不等于 y"
else
   echo "${x} != ${y}: x 等于 y"
fi

if [[ -z ${x} ]]; then
   echo "-z ${x} : 字符串长度为 0"
else
   echo "-z ${x} : 字符串长度不为 0"
fi

if [[ -n "${x}" ]]; then
   echo "-n ${x} : 字符串长度不为 0"
else
   echo "-n ${x} : 字符串长度为 0"
fi

if [[ ${x} ]]; then
   echo "${x} : 字符串不为空"
else
   echo "${x} : 字符串为空"
fi

#  Output:
#  x=abc, y=xyz
#  abc = xyz: x 不等于 y
#  abc != xyz : x 不等于 y
#  -z abc : 字符串长度不为 0
#  -n abc : 字符串长度不为 0
#  abc : 字符串不为空
```



```Bash
#!/bin/bash

a="abc"
b="efg"

if [ $a = $b ]
then
   echo "$a = $b : a 等于 b"
else
   echo "$a = $b: a 不等于 b"  #
fi
```



**字符串截取**

```Shell
#!/bin/bash

logpath='home/test/shell/shell-test.log'
url='https://www.test.com/blog/shell-test'
# 输出字符串长度
echo ${#logpath} ${#url}  #30 36

# 截取最后一个/后的值
log_suffix=${logpath##*/}
echo $log_suffix  #shell-test.log
# 截取第一个/后的值
url_suffix=${url#*/}
echo $url_suffix  #/www.test.com/blog/shell-test

# 截取第一个/前的值
log_prefix=${logpath%%/*}
echo $log_prefix  #home
# 截取最后一个/前的值
url_prefix=${url%/*}
echo $url_prefix  #https://www.test.com/blog

# 自定义截取
sublogpath=${logpath:0:5}
suburl=${url:0:8}
echo $sublogpath '***' $suburl  #home/ *** https://
# 从左边第9个字符开始到最后
sublogpath=${logpath:8}
suburl=${url:8}
echo $sublogpath '***' $suburl  #t/shell/shell-test.log *** www.test.com/blog/shell-test
# 从右边第9个字符开始截取5个字符
sublogpath=${logpath:0-9:5}
suburl=${url:0-9:5}
echo $sublogpath '***' $suburl  #-test *** hell-
```





### 数组

- 只支持一维数组

- `array=(value0 value1 value2 value3)`

    - 单独定义：`array[0]=value0`

- 读取数组：`valuen=${array_name[n]}`

    - 获取数组中的所有元素：`${array[@]}`

    - 获取数组长度：`length=${#array[@]}`或`length=${#array[*]}`

    - 获取单个元素长度：`length=${#array[n]}`





bash 只支持一维数组。

数组下标从 0 开始，下标可以是整数或算术表达式，其值应大于或等于 0。

**创建数组**

```Shell
# 创建数组的不同方式
nums=([2]=2 [0]=0 [1]=1)
colors=(red yellow "dark blue")
```

**访问数组元素**

- **访问数组的单个元素：**

```Shell
echo ${nums[1]}
Output: 1
```



- **访问数组的所有元素：**

```Shell
echo ${colors[*]}
Output: red yellow dark blue

echo ${colors[@]}
Output: red yellow dark blue
```

上面两行有很重要（也很微妙）的区别：

为了将数组中每个元素单独一行输出，我们用 `printf` 命令：

```Shell
printf "+ %s\n" ${colors[*]}
Output:
+ red
+ yellow
+ dark
+ blue
```

为什么dark和blue各占了一行？尝试用引号包起来：

```Shell
printf "+ %s\n" "${colors[*]}"
Output:
+ red yellow dark blue
```

现在所有的元素都在一行输出 —— 这不是我们想要的！让我们试试`${colors[@]}`

```Shell
printf "+ %s\n" "${colors[@]}"
Output:
+ red
+ yellow
+ dark blue
```

在引号内，`${colors[@]}`将数组中的每个元素扩展为一个单独的参数；数组元素中的空格得以保留。

- **访问数组的部分元素：**

```Shell
echo ${nums[@]:0:2}
Output:
0 1
```

在上面的例子中，`${array[@]}` 扩展为整个数组，`:0:2`取出了数组中从 0 开始，长度为 2 的元素。

**访问数组长度**

```Shell
echo ${#nums[*]}
Output:
3
```

### 向数组中添加元素

向数组中添加元素也非常简单：

```Shell
colors=(white "${colors[@]}" green black)
echo ${colors[@]}
Output:
white red yellow dark blue green black
```

上面的例子中，`${colors[@]}` 扩展为整个数组，并被置换到复合赋值语句中，接着，对数组`colors`的赋值覆盖了它原来的值。

### 从数组中删除元素

用`unset`命令来从数组中删除一个元素：

```Shell
unset nums[0]
echo ${nums[@]}
Output:
1 2
```

**💻 『示例源码』**

```Shell
#!/usr/bin/env bash

################### 创建数组 ###################
nums=( [ 2 ] = 2 [ 0 ] = 0 [ 1 ] = 1 )
colors=( red yellow "dark blue" )

################### 访问数组的单个元素 ###################
echo ${nums[1]}
# Output: 1

################### 访问数组的所有元素 ###################
echo ${colors[*]}
# Output: red yellow dark blue

echo ${colors[@]}
# Output: red yellow dark blue

printf "+ %s\n" ${colors[*]}
# Output:
# + red
# + yellow
# + dark
# + blue

printf "+ %s\n" "${colors[*]}"
# Output:
# + red yellow dark blue

printf "+ %s\n" "${colors[@]}"
# Output:
# + red
# + yellow
# + dark blue

################### 访问数组的部分元素 ###################
echo ${nums[@]:0:2}
# Output:
# 0 1

################### 获取数组长度 ###################
echo ${#nums[*]}
# Output:
# 3

################### 向数组中添加元素 ###################
colors=( white "${colors[@]}" green black )
echo ${colors[@]}
# Output:
# white red yellow dark blue green black

################### 从数组中删除元素 ###################
unset nums[ 0 ]
echo ${nums[@]}
# Output:
# 1 2
```





### 文件检测

- `[ -d $file ]` 文件是否是目录

- `[ -r $file ]` 文件是否可读

- `[ -w $file ]` 文件是否可写

- `[ -x $file ]` 文件是否可执行

- `[ -f $file ]` 文件是否是普通文件（既不是目录，也不是设备文件）

- `[ -s $file ]` 文件是否为空（文件大小是否大于0）

- `[ -e $file ]` 文件（包括目录）是否存在



文件测试运算符用于检测 Unix 文件的各种属性。

属性检测描述如下：

**💻 『示例源码』**

```Bash
file="/etc/hosts"

if [[ -r ${file} ]]; then
   echo "${file} 文件可读"
else
   echo "${file} 文件不可读"
fi
if [[ -w ${file} ]]; then
   echo "${file} 文件可写"
else
   echo "${file} 文件不可写"
fi
if [[ -x ${file} ]]; then
   echo "${file} 文件可执行"
else
   echo "${file} 文件不可执行"
fi
if [[ -f ${file} ]]; then
   echo "${file} 文件为普通文件"
else
   echo "${file} 文件为特殊文件"
fi
if [[ -d ${file} ]]; then
   echo "${file} 文件是个目录"
else
   echo "${file} 文件不是个目录"
fi
if [[ -s ${file} ]]; then
   echo "${file} 文件不为空"
else
   echo "${file} 文件为空"
fi
if [[ -e ${file} ]]; then
   echo "${file} 文件存在"
else
   echo "${file} 文件不存在"
fi

#  Output:(根据文件的实际情况，输出结果可能不同)
#  /etc/hosts 文件可读
#  /etc/hosts 文件可写
#  /etc/hosts 文件不可执行
#  /etc/hosts 文件为普通文件
#  /etc/hosts 文件不是个目录
#  /etc/hosts 文件不为空
#  /etc/hosts 文件存在
```











































## **函数**

bash 函数定义语法如下：

> 💡 说明：
> 
> 1. 函数定义时，`function` 关键字可有可无。
> 
> 2. 函数返回值 - return 返回函数返回值，返回值类型只能为整数（0-255）。如果不加 return 语句，shell 默认将以最后一条命令的运行结果，作为函数返回值。
> 
> 3. 函数返回值在调用该函数后通过 `$?` 来获得。
> 
> 4. 所有函数在使用前必须定义。这意味着必须将函数放在脚本开始部分，直至 shell 解释器首次发现它时，才可以使用。调用函数仅使用其函数名即可。
> 
> 

**💻 『示例源码』**

```Bash
#!/usr/bin/env bash

calc(){
  PS3="choose the oper: "
  select oper in + - * / # 生成操作符选择菜单
  do
  echo -n "enter first num: " && read x # 读取输入参数
  echo -n "enter second num: " && read y # 读取输入参数
  exec
  case ${oper} in
    "+")
      return $((${x} + ${y}))
    ;;
    "-")
      return $((${x} - ${y}))
    ;;
    "*")
      return $((${x} * ${y}))
    ;;
    "/")
      return $((${x} / ${y}))
    ;;
    *)
      echo "${oper} is not support!"
      return 0
    ;;
  esac
  break
  done
}
calc
echo "the result is: $?" # $? 获取 calc 函数返回值
```

执行结果

```Shell
$ ./function-demo.sh
1) +
2) -
3) *
4) /
choose the oper: 3
enter first num: 10
enter second num: 10
the result is: 100
```



```Bash
#!/bin/bash

# 输入1个整数，打印出比输入小的整数

function printNumber () {
  i=0;
  while [ $i -lt $1 ]
  do
    echo $i;
    i=$(($i+1))
    sleep 1;
  done
  return 0;  
}

read -p "请输入一个整数:" n;
printNumber $n;

```



### 位置参数

**位置参数**是在调用一个函数并传给它参数时创建的变量。

位置参数变量表：

**💻 『示例源码』**

```Bash
#!/usr/bin/env bash

x=0
if [[ -n $1 ]]; then
  echo "第一个参数为：$1"
  x=$1
else
  echo "第一个参数为空"
fi

y=0
if [[ -n $2 ]]; then
  echo "第二个参数为：$2"
  y=$2
else
  echo "第二个参数为空"
fi

paramsFunction(){
  echo "函数第一个入参：$1"
  echo "函数第二个入参：$2"
}
paramsFunction ${x} ${y}
```

执行结果

```Shell
$ ./function-demo2.sh
第一个参数为空
第二个参数为空
函数第一个入参：0
函数第二个入参：0

$ ./function-demo2.sh 10 20
第一个参数为：10
第二个参数为：20
函数第一个入参：10
函数第二个入参：20
```

执行 `./variable-demo4.sh hello world` ，然后在脚本中通过 `$1`、`$2` ... 读取第 1 个参数、第 2 个参数。。。

### 函数处理参数

另外，还有几个特殊字符用来处理参数：

**💻 『示例源码』**

```Bash
runner() {
  return 0
}

name=zp
paramsFunction(){
  echo "函数第一个入参：$1"
  echo "函数第二个入参：$2"
  echo "传递到脚本的参数个数：$#"
  echo "所有参数："
  printf "+ %s\n" "$*"
  echo "脚本运行的当前进程 ID 号：$$"
  echo "后台运行的最后一个进程的 ID 号：$!"
  echo "所有参数："
  printf "+ %s\n" "$@"
  echo "Shell 使用的当前选项：$-"
  runner
  echo "runner 函数的返回值：$?"
}
paramsFunction 1 "abc" "hello, \"zp\""
#  Output:
#  函数第一个入参：1
#  函数第二个入参：abc
#  传递到脚本的参数个数：3
#  所有参数：
#  + 1 abc hello, "zp"
#  脚本运行的当前进程 ID 号：26400
#  后台运行的最后一个进程的 ID 号：
#  所有参数：
#  + 1
#  + abc
#  + hello, "zp"
#  Shell 使用的当前选项：hB
#  runner 函数的返回值：0
```



```Shell
#!/bin/bash
echo "hello world"
#!/bin/bash

funWithParam(){
    echo "第一个参数为 $1 !"
    echo "第二个参数为 $2 !"
    echo "第十个参数为 ${10} !"
    echo "第十一个参数为 ${11} !"
    echo "参数总数有 $# 个!"
    echo "作为一个字符串输出所有参数 $* !"
}

funWithParam 1 2 3 4 5 6 7 8 9 34 73

# hello world
# 第一个参数为 1 !
# 第二个参数为 2 !
# 第十个参数为 34 !
# 第十一个参数为 73 !
# 参数总数有 11 个!
# 作为一个字符串输出所有参数 1 2 3 4 5 6 7 8 9 34 73 !
```









**系统函数**

1. **basename**

    - **基本语法**

basename [string / pathname] [suffix]   （功能描述：basename命令会删掉所有的前缀包括最后一个（‘/’）字符，然后将字符串显示出来）

basename 可以理解为取路径里的文件名称。

选项：

suffix为后缀，如果suffix被指定了，basename会将pathname或string中的suffix去掉。

- **案例实操**

截取该/home/atguigu/banzhang.txt路径的文件名称。

[atguigu@hadoop101 shells]$ basename /home/atguigu/banzhang.txt 

banzhang.txt

[atguigu@hadoop101 shells]$ basename /home/atguigu/banzhang.txt .txt

banzhang

4. **dirname**

    - **基本语法**

dirname 文件绝对路径  （功能描述：从给定的包含绝对路径的文件名中去除文件名（非目录的部分），然后返回剩下的路径（目录的部分））

dirname 可以理解为取文件路径的绝对路径名称。

- **案例实操**

获取banzhang.txt文件的路径。

[atguigu@hadoop101 \~]$ dirname /home/atguigu/banzhang.txt 

/home/atguigu

5. **自定义函数**

    - **基本语法**

[ function ] funname[()]

\{

Action;

[return int;]

\}

- **经验技巧**

    - 在调用函数地方之前，必须先声明函数。shell脚本是逐行运行，不会像其它语言一样先编译。

    - 函数返回值，只能通过$?系统变量获得，可以显示加：return返回，如果不加，将以最后一条命令运行结果，作为返回值。return后跟数值n（0-255）。

- **案例实操**

计算两个输入参数的和。

[atguigu@hadoop101 shells]$ touch fun.sh

[atguigu@hadoop101 shells]$ vim fun.sh



\#\!/bin/bash

function sum()

\{

s=0

s=$[$1\+$2]
    echo "$s"

\}



read -p "Please input the number1: " n1;

read -p "Please input the number2: " n2;

sum $n1 $n2;



[atguigu@hadoop101 shells]$ chmod 777 fun.sh

[atguigu@hadoop101 shells]$ ./fun.sh 

Please input the number1: 2

Please input the number2: 5

7









## **Shell工具**

## **cut**

cut的工作就是“剪”，具体的说就是在文件中负责剪切数据。cut 命令从文件的每一行剪切字节、字符和字段并将这些字节、字符和字段输出。

- **基本用法**

cut  [选项参数]  filename

说明：默认分隔符是制表符

- **选项参数说明**

- **案例实操**

    - 数据准备。

[atguigu@hadoop101 shells]$ touch cut.txt

[atguigu@hadoop101 shells]$ vim cut.txt

dong shen

guan zhen

wo  wo

lai  lai

le  le

- 切割cut.txt第一列。

[atguigu@hadoop101 shells]$ cut -d " " -f 1 cut.txt 

dong

guan

wo

lai

le

- 切割cut.txt第二、三列。

[atguigu@hadoop101 shells]$ cut -d " " -f 2,3 cut.txt

Le 

- 在cut.txt文件中切割出guan。

[atguigu@hadoop101 shells]$  cat cut.txt \|grep guan \| cut -d " " -f 1

guan

- 选取系统PATH变量值，第2个“：”开始后的所有路径。

[atguigu@hadoop101 shells]$ echo $PATH

/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/atguigu/.local/bin:/home/atguigu/bin



[atguigu@hadoop101 shells]$ echo $PATH \| cut -d ":" -f 3-

/usr/local/sbin:/usr/sbin:/home/atguigu/.local/bin:/home/atguigu/bin

- 切割ifconfig 后打印的IP地址。

[atguigu@hadoop101 shells]$ ifconfig ens33 \| grep netmask \| cut -d "i" -f 2 \| cut -d " " -f 2

192.168.6.101

6. **awk**

一个强大的文本分析工具，把文件逐行的读入，以空格为默认分隔符将每行切片，切开的部分再进行分析处理。

- **基本用法**

awk  [选项参数] ‘/pattern1/\{action1\}  /pattern2/\{action2\}...’ filename

pattern：表示awk在数据中查找的内容，就是匹配模式。

action：在找到匹配内容时所执行的一系列命令。

- **选项参数说明**

- **案例实操**

    - 数据准备。

[atguigu@hadoop101 shells]$ sudo cp /etc/passwd ./

passwd数据的含义

用户名:密码(加密过后的):用户id:组id:注释:用户家目录:shell解析器

- 搜索passwd文件以root关键字开头的所有行，并输出该行的第7列。

[atguigu@hadoop101 shells]$ awk -F : '/^root/\{print $7\}' passwd 

/bin/bash

- 搜索passwd文件以root关键字开头的所有行，并输出该行的第1列和第7列，中间以“，”号分割。

[atguigu@hadoop101 shells]$ awk -F : '/^root/\{print $1","$7\}' passwd 

root,/bin/bash

注意：只有匹配了pattern的行才会执行action。

- 只显示/etc/passwd的第一列和第七列，以逗号分割，且在所有行前面添加列名user，shell在最后一行添加"dahaige，/bin/zuishuai"。

[atguigu@hadoop101 shells]$ awk -F : 'BEGIN\{print "user, shell"\} \{print $1","$7\} END\{print "dahaige,/bin/zuishuai"\}' passwd

user, shell

root,/bin/bash

bin,/sbin/nologin

。。。

atguigu,/bin/bash

dahaige,/bin/zuishuai

注意：BEGIN 在所有数据读取行之前执行；END 在所有数据执行之后执行。

- 将passwd文件中的用户id增加数值1并输出

[atguigu@hadoop101 shells]$ awk -v i=1 -F : '\{print $3\+i\}' passwd

1

2

3

4

- **awk的内置变量**

- **案例实操**

    - 统计passwd文件名，每行的行号，每行的列数。

[atguigu@hadoop101 shells]$ awk -F : '\{print "filename:" FILENAME  ",linenum:" NR ",col:"NF\}' passwd 

filename:passwd,linenum:1,col:7

filename:passwd,linenum:2,col:7

filename:passwd,linenum:3,col:7

。。。

- 查询ifconfig命令输出结果中的空行所在的行号。

[atguigu@hadoop101 shells]$ ifconfig \| awk '/^$/\{print NR\}'

9

18

26

- 切割IP。

[atguigu@hadoop101 shells]$ ifconfig ens33 \| grep netmask \| awk -F "inet" '\{print $2\}' \| awk -F " " '\{print $1\}' 

192.168.6.101





## **正则表达式入门**

正则表达式使用单个字符串来描述、匹配一系列符合某个语法规则的字符串。在很多文本编辑器里，正则表达式通常被用来检索、替换那些符合某个模式的文本。在Linux中，grep、sed、awk等命令都支持通过正则表达式进行模式匹配。

7. **常规匹配**

一串不包含特殊字符的正则表达式匹配它自己，例如：

[atguigu@hadoop101 shells]$ cat /etc/passwd \| grep atguigu

就会匹配所有包含atguigu的行。

8. **常用特殊字符**

    - **特殊字符：**^

^ 匹配一行的开头，例如：

[atguigu@hadoop101 shells]$ cat /etc/passwd \| grep ^a

会匹配出所有以a开头的行。

- **特殊字符：**$

$ 匹配一行的结束，例如：

[atguigu@hadoop101 shells]$ cat /etc/passwd | grep t$

会匹配出所有以t结尾的行。

思考：^$ 匹配什么？

- **特殊字符：**.

. 匹配一个任意的字符，例如：

[atguigu@hadoop101 shells]$ cat /etc/passwd \| grep r..t

会匹配包含rabt,rbbt,rxdt,root等的所有行。

- **特殊字符：***

* 不单独使用，他和上一个字符连用，表示匹配上一个字符0次或多次，例如：

[atguigu@hadoop101 shells]$ cat /etc/passwd \| grep ro*t

会匹配rt, rot, root, rooot, roooot等所有行。

思考：.* 匹配什么？

- **特殊字符：**[ ]

[ ] 表示匹配某个范围内的一个字符，例如

[6,8]------匹配6或者8

[0-9]------匹配一个0-9的数字

[0-9]*------匹配任意长度的数字字符串

[a-z]------匹配一个a-z之间的字符

[a-z]* ------匹配任意长度的字母字符串

[a-c, e-f]-匹配a-c或者e-f之间的任意字符

[atguigu@hadoop101 shells]$ cat /etc/passwd \| grep r[a,b,c]*t

会匹配rt,rat, rbt, rabt, rbact,rabccbaaacbt等等所有行。

- **特殊字符：**\\

\\ 表示转义，并不会单独使用。由于所有特殊字符都有其特定匹配模式，当我们想匹配某一特殊字符本身时（例如，我想找出所有包含 '$' 的行），就会碰到困难。此时我们就要将转义字符和特殊字符连用，来表示特殊字符本身，例如。

[atguigu@hadoop101 shells]$ cat /etc/passwd \| grep a\\$b

就会匹配所有包含 a$b 的行。

9. **其他特殊字符**

见参考资料的正则表达式语法。











## 加载外部脚本

- `. filename` 或 `source filename`

```Bash
#!/bin/bash
# test1.sh

url="http://www.test1.com"

```

```Bash
#!/bin/bash
#test2.sh

#使用 . 号来引用test1.sh 文件
. ./test1.sh

或者使用以下包含文件代码
source ./test1.sh

echo "path：$url"

#输出：
$ ./test2.sh 
path：http://www.test1.com
```







## 高级命令



### test

> - 用于检查某个条件是否成立，可以进行数值、字符、文件三个方面的测试
> 
> 

```Bash
#!/bin/bash
num1=100
num2=100
if test $[num1] -eq $[num2]
then
    echo '两个数相等！' #
else
    echo '两个数不相等！'
fi
```



### awk

```Shell
# test.log
2 this is a test
3 Are you like awk
This's a test
10 There are orange,apple,mongo
```

- 用法1：`awk '{[pattern] action}' {filenames}`   \# 行匹配语句 awk '' 只能用单引号

```Shell
# 1、每行按空格或TAB分割，输出文本中的1、4项
$ awk '{print $1,$4}' test.log
#-------------------输出--------------------------
2 a
3 like
This's
10 orange,apple,mongo

# 2、格式化输出
$ awk '{printf "%-8s %-10s\n",$1,$4}' test.log
#---------------------输出------------------------
2        a
3        like
This's
10       orange,apple,mongo
```





- 用法2：`awk -F`  \#-F相当于内置变量FS, 指定分割字符

```Bash
# 1、使用","分割
$  awk -F, '{print $1,$2}'   test.log
#--------------------输出-------------------------
2 this is a test
3 Are you like awk
This's a test
10 There are orange apple

# 2、或者使用内建变量
$ awk 'BEGIN{FS=","} {print $1,$2}'     test.log
-----------------------输出----------------------
2 this is a test
3 Are you like awk
This's a test
10 There are orange apple

# 3、使用多个分隔符.先使用空格分割，然后对分割结果再使用","分割
$ awk -F '[ ,]'  '{print $1,$2,$5}'   test.log
#-----------------------输出----------------------
2 this test
3 Are awk
This's a
10 There apple
```

- 用法3：`awk -v`  \# 设置变量

```Bash
$ awk -va=1 '{print $1,$1+a}' test.log
#--------------------输出-------------------------
2 3
3 4
This's 1
10 11

$ awk -va=1 -vb=s '{print $1,$1+a,$1b}' test.log
#-------------------输出--------------------------
2 3 2s
3 4 3s
This's 1 This'ss
10 11 10s
```

- 用法4：`awk -f {awk脚本} {文件名}`

```Shell
$ awk -f cal.awk test.log
```

- 过滤第一列大于2的行

```Shell
$ awk '$1>2' test.log    #命令

#输出
3 Are you like awk
This's a test
10 There are orange,apple,mongo
```

- 过滤第一列等于2的行

```Shell
$ awk '$1==2 {print $1,$3}' test.log    #命令

#输出
2 is
```

- 过滤第一列大于2并且第二列等于'Are'的行

```Shell
$ awk '$1>2 && $2=="Are" {print $1,$2,$3}' test.log    #命令

#输出
3 Are you
```

- 输出第二列包含 "th"，并打印第二列与第四列

```Shell
$ awk '$2 ~ /th/ {print $2,$4}' test.log

#---------------------------------------------
this a
```

- 输出包含 "re" 的行

```Shell
$ awk '/re/ ' test.log

# ~ 表示模式开始。// 中是模式。
#---------------------------------------------
3 Are you like awk
10 There are orange,apple,mongo
```

- 忽略大小写

```Shell
$ awk 'BEGIN{IGNORECASE=1} /this/' test.log

#---------------------------------------------
2 this is a test
This's a test
```

- 模式取反

```SQL
$ awk '$2 !~ /th/ {print $2,$4}' test.log
#---------------------------------------------
Are like
a
There orange,apple,mongo

$ awk '!/th/ {print $2,$4}' test.log
#---------------------------------------------
Are like
a
There orange,apple,mongo
```

### xargs

给命令传递参数的过滤器，将标准输入（stdin）数据转化为命令行参数，一般和管道`|`一起使用。

- `-a`：file 从文件中读入作为sdtin

- `-e`：flag ，注意有的时候可能会是-E，flag必须是一个以空格分隔的标志，当xargs分析到含有flag这个标志的时候就停止。

- `-p`：当每次执行一个argument的时候询问一次用户。

- `-n`：num 后面加次数，表示命令在执行的时候一次用的argument的个数，默认是用所有的。

- `-t`：表示先打印命令，然后再执行。

- `-i`：或者是-I，这得看linux支持了，将xargs的每项名称，一般是一行一行赋值给 \{\}，可以用 \{\} 代替。

- `-r`：no-run-if-empty 当xargs的输入为空的时候则停止xargs，不用再去执行了。

- `-s`：num 命令行的最大字符数，指的是 xargs 后面那个命令的最大命令行字符数。

- `-L`：num 从标准输入一次读取 num 行送给 command 命令。

- `-l`：同 -L。

- `-d`：delim 分隔符，默认的xargs分隔符是回车，argument的分隔符是空格，这里修改的是xargs的分隔符。

- `-x`：exit的意思，主要是配合-s使用。。

- `-P`：修改最大的进程数，默认是1，为0时候为as many as it can ，这个例子我没有想到，应该平时都用不到的吧。

```Markdown
# cat test.log
a b c d e
f g h i j
k l

#多行输入单行输出：
# cat test.txt | xargs
a b c d e f g h i j k l

# cat test.txt | xargs -n3
a b c
d e f
g h i
j k l

# echo "nameXnameXnameXname" | xargs -dX
name name name name

# echo "nameXnameXnameXname" | xargs -dX -n2
name name
name name

#复制所有图片文件到 /data/images 目录下：
ls *.jpg | xargs -n1 -I {} cp {} /data/images

#用 rm 删除太多的文件时候，可能得到一个错误信息：/bin/rm Argument list too long. 用 xargs 去避免这个问题：
find . -type f -name "*.log" -print0 | xargs -0 rm -f
# -print0：指定输出的文件列表以null分隔。
# xargs命令的-0参数表示用null当作分隔符

#统计一个源代码目录中所有 php 文件的行数：
find . -type f -name "*.php" -print0 | xargs -0 wc -l

#查找所有的 jpg 文件，并且压缩它们：
find . -type f -name "*.jpg" -print | xargs tar -czvf images.tar.gz

#假如你有一个文件包含了很多你希望下载的 URL，你能够使用 xargs下载所有链接：
cat url-list.txt | xargs wget -c
```

### 编辑文件sed

- 参数：

    - `-e<script> 或--expression=<script>` 以选项中指定的script来处理输入的文本文件。

    - `-f<script文件> 或--file=<script文件>` 以选项中指定的script文件来处理输入的文本文件。

    - `-h 或--help` 显示帮助。

    - `-n 或--quiet或--silent` 仅显示script处理后的结果。

    - `-V 或--version` 显示版本信息。

- 动作：

    - `a`：新增， a 的后面可以接字串，而这些字串会在新的一行出现(目前的下一行)～

    - `c`：取代， c 的后面可以接字串，这些字串可以取代 n1,n2 之间的行！

    - `d`：删除， d 后面通常不接任何东西；

    - `i`：插入， i 的后面可以接字串，而这些字串会在新的一行出现(目前的上一行)；

    - `p`：打印，亦即将某个选择的数据印出。通常 p 会与参数 sed -n 一起运行～

    - `s`：取代，可以直接进行取代的工作，通常这个 s 的动作可以搭配正规表示法！例如 1,20s/old/new/g

```Bash
#!/usr/bin/env bash
LOGPATH='/home/test/shell/'
TEST_LOG="${LOGPATH}test.log"
#$TEST_LOG初始内容
## abc.
## def.
## ghi.
## jkl.

# 在TEST_LOG文件的第四行后添加一行，并将结果输出到标准输出
sed -e 4a\newLine $TEST_LOG
## ...
## jkl
## newLine

# 将 TEST_LOG 的内容列出并且列印行号，同时，请将第 2~5 行删除！
nl $TEST_LOG | sed -e '2,5d'
# 删除第 3 到最后一行($：代表最后一行)
nl $TEST_LOG | sed -e '3,$d'
# 在第二行后(亦即是加在第三行)加上『drink tea?』字样！
nl $TEST_LOG | sed -e '2a drink tea'
# 在第二行前加上『drink tea?』字样！
nl $TEST_LOG | sed -e '2i drink tea'
# 在第4行之后追加 3 行(2 行文字和 1 行空行)
sed -e '4 a newline\nnewline2\n' $TEST_LOG

# 将第2-5行的内容替换成为『No 2-5 number』
nl $TEST_LOG | sed '2,5c No 2-5 number'

# 搜索$TEST_LOG有root关键字的行，只输出匹配行
nl $TEST_LOG | sed -n '/root/p'

# 删除$TEST_LOG所有包含root的行，其他行输出
nl $TEST_LOG | sed  '/root/d'

# 搜索$TEST_LOG,找到root对应的行，执行后面花括号中的一组命令，每个命令之间用分号分隔
# 这里把bash替换为blueshell，再输出这行,q表示退出
nl $TEST_LOG | sed -n '/root/{s/bash/blueshell/;p;q}'

# 一条sed命令，删除$TEST_LOG第3行到末尾的数据，并把bash替换为blueshell
nl $TEST_LOG | sed -e '3,$d' -e 's/bash/blueshell/'


# 数据的搜寻并替换
# 格式：sed 's/要被取代的字串/新的字串/g'
# 替换多个格式：sed 's/要被取代的字串/新的字串/g;s/source2/target2/g;s/source3/target3/g'

# 查询本机ip，将IP前面和后面的部分删除，过滤出ip地址（inet addr:192.168.1.100 Bcast:192.168.1.255 Mask:255.255.255.0）
/sbin/ifconfig eth0 | grep 'inet addr' | sed 's/^.*addr://g' | sed 's/Bcast.*$//g'


# 修改文件内容
# 将$TEST_LOG中每行结尾的.替换成！
sed -i 's/.$/\!/g' $TEST_LOG
# 在$TEST_LOG最后一行添加 #This is a test
sed -i '$a # This is a test' $TEST_LOG

```





## 面试题

1.1 Linux\&Shell

1.1.1 Linux常用高级命令

1.1.2 Shell常用工具及写过的脚本

1）awk、sed、cut、sort

2）用Shell写过哪些脚本

（1）集群启动，分发脚本

\#\!/bin/bash



case $1 in 

"start")

for i in hadoop102 hadoop103 hadoop104

do

ssh $i "绝对路径"

done 

;;

"stop")



;;

（2）数仓层级内部的导入：ods-\>dwd-\>dws -\>ads

①\#\!/bin/bash 

②定义变量 APP=gmall

③获取时间    传入  按照传入时间

不传  T\+1 

④sql="

先按照当前天 写sql =\> 遇到时间 $do_date  遇到表 \{$APP\}.

自定义函数 UDF  UDTF    \{$APP\}.

"

⑤执行sql

1.1.3 Shell中单引号和双引号区别

1）在/home/atguigu/bin创建一个test.sh文件

[atguigu@hadoop102 bin]$ vim test.sh

在文件中添加如下内容

\#\!/bin/bash

do_date=$1



echo '$do_date'

echo "$do_date"

echo "'$do_date'"

echo '"$do_date"'

echo `date`

2）查看执行结果

[atguigu@hadoop102 bin]$ test.sh 2022-02-10

$do_date

2022-02-10

'2022-02-10'

"$do_date"

2022年 05月 02日 星期四 21:02:08 CST

3）总结：

（1）单引号不取变量值

（2）双引号取变量值

（3）反引号\`，执行引号中命令

（4）双引号内部嵌套单引号，取出变量值

（5）单引号内部嵌套双引号，不取出变量值


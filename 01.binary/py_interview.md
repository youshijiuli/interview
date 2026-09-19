##### 位和字节的关系
* 8位=一字节

##### b、B、kB、MB、GB的关系
1. 1B=8b
2. 1kB=1024B
3. 1MB=1024kB
4. 1GB=1024MB

---

##### 编写一个函数实现十进制转62进制，分别用0-9A-Za-z,表示62位字母
```python
import string
print(string.ascii_lowercase) # 小写字母
print(string.ascii_uppercase) # 大写字母
print(string.digits) # 0-9

s=string.digits+string.ascii_uppercase+string.ascii_lowercase
def _10_to_62(num):
    ss=''
    while True:
        ss=s[num%62]+ss
        if num//62==0:
            break
        num=num//62
    return ss
print(_10_to_62(65))
```

---

##### 字节码和机器码的区别
* 机器码是电脑CPU直接读取运行的机器指令，运行速度最快，但是非常晦涩难懂，也比较难编写，一般从业人员接触不到。
* 字节码是一种中间状态（中间码）的二进制代码（文件）。需要直译器转译后才能成为机器码。

---

##### python中进制转换
>进制转换以十进制为媒介
>十六进制前面加上0x，八进制加上0o，二进制前面加上0b

||二进制|八进制|十进制|十六进制|
| --- | --- | --- | --- | --- |
| 二进制 | |bin(int(x, 8)）  | bin(int(x, 10))  | bin(int(x, 16)) |
| 八进制 | oct(int(x, 2)) |  | oct(int(x, 10)) |oct(int(x, 16))  |
|十进制  | int(x, 2) | int(x, 8) |  | int(x, 16) |
| 十六进制 | hex(int(x, 2))|hex(int(x, 8))|hex(int(x, 10)) |

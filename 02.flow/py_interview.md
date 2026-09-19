##### 实现99乘法表（使用两种方法）
```python
print('\n'.join(['\t'.join(['{}*{}={}'.format(x,y,x*y) for x in range(1,y+1)]) for y in range(1,10)]))
```
```python
for i in range(1,10):
    for j in range(1,i+1):
        print('%s*%s=%s'%(i,j,i*j),end='\t')
    else:
        print()
```

---

##### pass的使用
* 通常用来标记一个还未写的代码的位置，pass不做任何事情，一般用来做占位语句，保持程序结构的完整性

---

##### 三元运算编写格式
* 表达式1 if 布尔表达式2 else 表达式3
* 例如：a=3 if 3 > 4 else 5

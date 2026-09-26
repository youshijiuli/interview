##### 二叉树是非线性结构，栈和队列以及线性表都是线性结构，对吗？
* 对的

---

##### 解决哈希冲突的算法有哪几种？分别有什么特点？
[哈希冲突参考](https://blog.csdn.net/seulzz/article/details/77163878)
1. 开放定址法
2. 再哈希法
3. 链地址法
4. 建立公共溢出区

---

##### 写一个函数，计算出以下字母所代表的数字，每个字母值不一样
```python
for A in range(1,10):
    for B in range(10):
        if A==B:
            continue
        for C in range(1,10):
            if C in [A,B]:
                continue
            for D in range(10):
                if D in [A,B,C]:
                    continue
                for E in range(1,10):
                    if E in [A,B,C,D]:
                        continue
                    for F in range(10):
                        if F in [A,B,C,D,E]:
                            continue
                        for G in range(1,10):
                            if G in [A,B,C,D,E,F]:
                                continue
                            for H in range(10):
                                if H in [A,B,C,D,E,F,G]:
                                    continue
                                for P in range(1,10):
                                    if P in [A,B,C,D,E,F,G,H]:
                                        continue
                                    if (A*10+B)-(C*10+D)==(E*10+F) and (E*10+F)+(G*10+H)==(P*100+P*10+P):
                                    print(A,B,C,D,E,F,G,H,P)
```

---

##### 输入一个字符串，输出该字符串的字符的所有组合。如输入'abc',输出a,b,c,ab,ac,bc,abc.

```python
def getC(s):
    if not s:
        return
    len_s=len(s)
    ss=[]
    for i in range(len_s):
        combination(s,0,i,ss)
aaa=[]
def combination(s,index,num,ss):
    global aaa
    if num==-1:
        return
    if index==len(s):
        return
    ss.append(s[index])
    aaa.append(''.join(ss))
    combination(s,index+1,num-1,ss)
    ss.pop()
    combination(s,index+1,num,ss)
    
getC('123')
print(aaa)
print(sorted(set(aaa),key=lambda x:len(str(x))))
```

---

##### 一个数如果恰好等于它的因子之和，这个数就称为‘完数’，比如6=1+2+3，编程找出1000以内的所有的完数。
```python
wanshu=[]
for i in range(1,1001):
    s=0
    for j in range(1,i//2+1):
        if i % j ==0:
            s+=j
    else:
        if i==s:
            wanshu.append(i)
print(wanshu)
```

---

##### 编写一个函数，找出数组中没有重复的值的和
```python
def func(lis):
    lis1=[]
    del_lis=[]
    for i in lis:
        if i not in lis1:
            if i not in del_lis:
                lis1.append(i)
        else:
            del_lis.append(i)
            lis1.remove(i)
    return sum(lis1)
    
def func2(lis):
    return sum([i for i in set(lis) if lis.count(i)==1])
    
print(func2([3,4,1,2,5,6,6,5,4,3,3]))
```

---

##### 给定一个非空的字符串，判断它是否可以由它的一个子串重复多次构成。给定的字符串只含有小写英文字母，并且长度不超过10000。例如：'ababab',返回True，'ababa'，返回False
```python
def solution(s):
    ll=len(s)
    for i in range(1,ll//2+1):
        if ll % i == 0:
            j=0
            while s[:i]==s[j:j+i] and j<ll:
                j=j+i
            if j==ll:
                return True
    return False
    
print(solution('abababa'))
```

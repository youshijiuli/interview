# python-面试通关宝典

### **算法和数据结构**

#### 114.已知：

```Python
AList = [1,2,3]
BSet = {1,2,3}
```

##### (1) 从 AList 和 BSet 中 查找 4，最坏时间复杂度那个大？

```
查找列表最坏时间复杂度是O(n),查找字典是O(1)，因为字典的数据结构是散列表
```

##### (2) 从 AList 和 BSet 中 插入 4，最坏时间复杂度那个大？

```
插入的操作都是O(1)
```

#### 115.用 Python 实现一个二分查找的函数。

```python
def binary_search(item,arr):
    start = 0
    end = len(arr) - 1
    while start <= end:
        mid = (start + end) // 2
        if item == arr[mid]:
            return True
        elif item < arr[mid]:
            end = mid - 1
        else:
            start = mid + 1
array = [1,2,3,4,5,6]
print(binary_search(2,array))
```

#### 116.Python 单例模式的实现方法。

```python
单例模式（Singleton Pattern）是一种常用的软件设计模式，该模式的主要目的是确保某一个类只有一个实例存在。当你希望在整个系统中，某个类只能出现一个实例时，单例对象就能派上用场。

比如，某个服务器程序的配置信息存放在一个文件中，客户端通过一个 AppConfig 的类来读取配置文件的信息。如果在程序运行期间，有很多地方都需要使用配置文件的内容，也就是说，很多地方都需要创建 AppConfig 对象的实例，这就导致系统中存在多个 AppConfig 的实例对象，而这样会严重浪费内存资源，尤其是在配置文件内容很多的情况下。事实上，类似 AppConfig 这样的类，我们希望在程序运行期间只存在一个实例对象
1.使用装饰器实现单例模式
def singleton(cls):
    _instance = {}
    def _singleton(*args,**kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args,**args)
        return _instance[cls]
    return _singleton
  
2.使用类实现单例模式
import threading
class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass


    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)  
        return Singleton._instanc
```

#### 117.使用 Python 实现一个斐波那契数列。

```Python
# 很多人上来就写下面这种解法
def fibnaqie(n):
    if n < 2:
        return n
    return fibnaqie(n - 1) + fibnaqie(n - 2)
# 这种解法时间复杂度高，而且一般不是面试官最想要的答案

# 下面这种优化的版本
def fib2(n):
    fib_n = 0
    fib_one = 1
    fib_two = 0
    res = [0, 1]
    if n < 2:
        return res[n]
    for i in range(2, n + 1):
        fib_n = fib_one + fib_two
        fib_two = fib_one
        fib_one = fib_n
    return fib_n
# 所以适当地选择递归还是迭代，要看具体情况，处理树，或者图的遍历的时候，递归还是比迭代优先考虑的
```

#### 118.找出列表中的重复数字。

```python
def find_duplicate(arr):
    not_dup = set()
    dup = set()
    for x in arr:
        if x not in not_dup:
            not_dup.add(x)
        else:
            dup.add(x)
    return dup


if __name__ == '__main__':
    array = [1, 2, 3, 4, 4, 4, 4]
    print(find_duplicate(array))
```

#### 119.找出列表中的单个数字。

```python
a = ['a', 1, 2, 'b']
for x in a:
    if str(x).isdigit():
        print(x)
```

#### 120.写一个冒泡排序。

```python
def bubble_sort(arr):
    n = len(arr)
    if len(arr) < 2:
        return arr
    for i in range(n - 1):
        count = 0
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                count += 1
        if count == 0:
            return arr
    return arr


if __name__ == '__main__':
    arr = [2, 1, 5, 3, 6]
    arr1 = [1, 2, 3, 4, 5]
    print(bubble_sort(arr1))
```

#### 121.写一个快速排序。

```python
def quick_sort(arr):
    if len(arr) < 2:
        return arr
    else:
        pivot = arr[0]
        less = [i for i in arr[1:] if i <= pivot]
        more = [i for i in arr[1:] if i > pivot]
    return quick_sort(less) + [pivot] + quick_sort(more)


if __name__ == '__main__':
    array = [2, 1, 6, 3, 4, 5]
    print(quick_sort(array))

```

#### 122.写一个拓扑排序。

```python
# 使用循环进行拓扑排序
def topoSort(G):
    # 初始化计算被指向节点的字典
    cnt = dict((u, 0) for u in G.keys())
    import pdb;pdb.set_trace()
    # 若某节点被其他节点指向，该节点计算量+1
    for u in G:
        for v in G[u]:
            cnt[v] += 1
    # 收集被指向数为0的节点,此时Q只有一个节点，即起始节点a
    Q = [u for u in cnt.keys() if cnt[u] == 0]
    # 记录结果
    seq = []
    while Q:
        s = Q.pop()
        seq.append(s)
        for u in G[s]:
            cnt[u] -= 1
            if cnt[u] == 0:
                Q.append(u)
    return seq


# 有向无环图的邻接字典
G = {
    'a': {'b', 'f'},
    'b': {'c', 'd', 'f'},
    'c': {'d'},
    'd': {'e', 'f'},
    'e': {'f'},
    'f': {}
}

res = topoSort(G)
print(res)

```

#### 123.用 Python 实现一个二进制计算。

```python
'''
以实现二进制加法为例
给定两个二进制字符串，返回他们的和（用二进制表示）。
输入为非空字符串且只包含数字 1 和 0。
输入: a = “11”, b = “1”
输出: “100”
'''


def binary_plus(a, b):
    a, b = int('0b' + a, 2), int('0b'+b, 2)
    return bin(a + b)[2:]


if __name__ == '__main__':
    a = '11'
    b = '1'
    print(binary_plus(a, b))

# 解释一下，class int(x, base) 
x–字符串或数字 
base–进制数，默认十进制。 
bin()函数返回一个整型int或者长整数long int的二进制表示，bin()运算返回的是二进制。所以前两位是二进制的标志，需要[2:]去除
```

#### 124.有一组 "+" 和 "-" 符号，要求将 "+" 排到左边，"-" 排到右边，写出具体的实现方法。

```python
def some_sort(arr):
    list_a = []
    list_b = []
    for x in arr:
        if x == '+':
            list_a.append(x)
        else:
            list_b.append(x)
    list_a.extend(list_b)
    print(list_a)
    return list_a
```

#### 125.单链表反转。

```python
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


def reverse_node(head):
    p = head
    q = head.next
    head.next = None
    while q:
        r = q.next
        q.next = p
        p = q
        q = r
    head = p
    return head


if __name__ == '__main__':
    l1 = ListNode(3)
    l1.next = ListNode(2)
    l1.next.next = ListNode(1)

    l = reverse_node(l1)
    print(l.val, l.next.val, l.next.next.val)
# 1,2,3
```

#### 126.交叉链表求交点。

```python
'''先遍历两个链表，获知两个链表各自的长度，往后调整较长链表的指针，使之与较短链表的起始指针对齐，然后两个链表同时往后扫描，直至二者的节点相同，证明该节点是相交节点，否则返回 None，表明两个链表不相交，时间复杂度o(n),空间复杂度0(1)'''
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


def solution(head_a, head_b):
    def get_list_length(head):
        len = 0
        while head:
            len += 1
            head = head.next
        return head

    def forward_long_list(long_len, short_len, head):
        delta = long_len - short_len
        while delta and head:
            head = head.next
            delta -= 1
        return head

    def main_func(head_a, head_b):
        head_a_len = get_list_length(head_a)
        head_b_len = get_list_length(head_b)
        if head_a_len > head_b_len:
            head_a = forward_long_list(head_a_len, head_b_len, head_a)
        else:
            head_b = forward_long_list(head_a_len, head_b_len, head_b)
        while head_a and head_b:
            if head_a == head_b:
                return head_a
            head_a = head_a.next
            head_b = head_b.next
        return None

    return main_func(head_a, head_b)


```

#### 127.用队列实现栈。

```python
class Stack:
    def __init__(self):
        self.queue_a = []
        self.queue_b = []

    def push(self, val):
        self.queue_a.append(val)

    def pop(self):
        if len(self.queue_a) == 0:
            return None
          # 核心思想就是留一个元素在队列a中，最后交换队列a,b，再从b中取栈顶元素
        while len(self.queue_a) != 1:
            self.queue_b.append(self.queue_a.pop(0))
        self.queue_a, self.queue_b = self.queue_b, self.queue_a
        return self.queue_b.pop()


test_stack = Stack()
for i in range(5):
    test_stack.push(i)
for i in range(5):
    print(test_stack.pop())

```

#### 128.找出数据流的中位数。

```python
# 中位数是有序列表中间的数。如果列表长度是偶数，中位数则是中间两个数的平均值
# 如果是奇数，则中位数就是中间的数字
def find_zhongwei(arr):
    arr.sort()
    if len(ar) == 0:
        return
    if len(ar) == 1:
        return ar[0]
    mid = len(arr) // 2
    if len(arr) % 2 == 0:
        return (arr[mid - 1] + arr[len(arr) / 2]) / 2
    else:
        return arr[mid]


if __name__ == '__main__':
    ar = [2, 1, 5, 3, 4]
    print(find_zhongwei(ar))

```

#### 129.二叉搜索树中第 K 小的元素。

```python
# 问题本质：对二叉树进行中序遍历，中序排序后，返回第K-1个值
class Solution(object):
    def kthSmallest(self, root, k):
        """
        :type root: TreeNode
        :type k: int
        :rtype: int
        """
        def inorderTraversal(root):
            if root is None:
                return []
            res = []
            res.extend(inorderTraversal(root.left))
            res.append(root.val)
            res.extend(inorderTraversal(root.right))
            return res
        return inorderTraversal(root)[k - 1]

```

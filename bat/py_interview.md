##### 使用两个队列实现一个栈
```python
class Stack(object):
    def __init__(self):
        self.queueA=[]
        self.queueB=[]
    def push(self,node):
        self.queueA.append(node)
    def pop(self):
        if len(self.queueA)==0:
            return None
        while len(self.queueA)!=1:
            self.queueB.append(self.queueA.pop(0))
        self.queueA,self.queueB=self.queueB,self.queueA
        return self.queueB.pop()
        
st=Stack()
print(st.pop())
st.push(1)
print(st.pop())
st.push(1)
st.push(1)
st.push(1)
print(st.pop())
print(st.pop())
print(st.pop())
```
* 注意上面两个栈的实现方法，第一种的效率高，队列的这种方法效率低

---

##### 有如下链表类，请实现单链表逆置。
```python
class ListNode:
    def __init__(self,val):
        self.val=val
        self.next=None
        
class Solution:
    def reverseList(self,pHead):
        if not pHead or not pHead.next:
            return pHead
        last=None
        while pHead:
            tmp=pHead.next
            pHead.next=last
            last=pHead
            pHead=tmp
        return last
```

---

##### 手写一个栈

```python
#给一个点，我们能够根据这个点知道一些内容
class Node(object):
    def __init__(self,val): #定位的点的值和一个指向
        self.val=val #指向元素的值,原队列第二元素
        self.next=None #指向的指针
        
class stack(object):
    def __init__(self):
        self.top=None #初始化最开始的位置
        
    def push(self,n):#添加到栈中
        n=Node(n) #实例化节点
        n.next=self.top #顶端元素传值给一个指针
        self.top=n
        return n.val
        
    def pop(self): #退出栈
        if self.top == None:
            return None
        else:
            tmp=self.top.val
            self.top=self.top.next #下移一位，进行
            return tmp
            
if __name__=="__main__":
    s=stack()
    print(s.pop())
    s.push(1)
    print(s.pop())
    s.push(2)
    s.push(3)
    print(s.pop())
    s.push(3)
    s.push(3)
    s.push(3)
    print(s.pop())
    print(s.pop())
    print(s.pop())
    print(s.pop())
```

---

##### 手写一个队列
```python
class Queue(object):
    def __init__(self,size):
        self.queue=[]
        self.size=size
    def is_empty(self):
        return not bool(len(self.queue))
    def is_full(self):
        return len(self.queue)==self.size
    def enqueue(self,val):
        if not self.is_full():
            self.queue.insert(0,val)
            return True
        return False
    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop()
        return None
s=Queue(2)
print(s.is_empty)
s.enqueue(1)
s.enqueue(2)
print(s.is_full())
print(s.dequeue())
print(s.dequeue())
print(s.is_empty())
```

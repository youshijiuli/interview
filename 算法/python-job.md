## 算法 排序

### 经典排序算法总结与实现  
最简单易懂的Python算法实现，带图示  
[经典排序算法总结与实现](http://wuchong.me/blog/2014/02/09/algorithm-sort-summary/)  

### 说一下冒泡排序？  
回答技巧:回答冒泡原理，最好能手写，拓展一下其他排序？  
冒泡排序的思想: 每次比较两个相邻的元素, 如果他们的顺序错误就把他们交换位置。  

### 冒泡排序 BubbleSort  
比较相邻的元素。如果第一个比第二个大，就交换他们两个。  
对第0个到第n-1个数据做同样的工作。这时，最大的数就“浮”到了数组最后的位置上。  
针对所有的元素重复以上的步骤，除了最后一个。  
持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较。  
```python
# 10000个随机数据耗时16s  
def maopao(l):  
    for i in range(1, len(l)):  
        for j in range(len(l) - i):  
            if l[j] > l[j + 1]:  
                l[j], l[j + 1] = l[j + 1], l[j]  
    print(l)   
```

### 选择排序 SelectionSort  
在未排序序列中找到最小（大）元素，存放到排序序列的起始位置。  
再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。  
以此类推，直到所有元素均排序完毕。  
```python
# 10000个随机数据耗时10s  
def xuanze(l):  
    for i in range(len(l)):  
        for j in range(i, len(l)):  
            if l[i] > l[j]:  
                l[i], l[j] = l[j], l[i]  
```
选择排序优化版  
```python
# 10000个随机数据耗时5s  
def xuanze_youhua(l):  
    for i in range(len(l)):  
        small_index = i  
        for j in range(i, len(l)):  
            if l[small_index] > l[j]:  
                small_index = j  
        l[i], l[small_index] = l[small_index], l[i]  
```

### 插入排序  
从第一个元素开始，该元素可以认为已经被排序  
取出下一个元素，在已经排序的元素序列中从后向前扫描  
如果被扫描的元素（已排序）大于新元素，将该元素后移一位  
重复步骤3，直到找到已排序的元素小于或者等于新元素的位置  
将新元素插入到该位置后  
重复步骤2~5  
```python
# 是否正确待确认  
# 10000个随机数据耗时10s  
def charu(l):  
    for i in range(1, len(l)):  
        for j in range(i):  
            if l[j] > l[i]:  
                l[j], l[i] = l[i], l[j]  
        print(l)  
```

### 快速排序  
快速排序通常明显比同为Ο(n log n)的其他算法更快，因此常被采用，而且快排采用了分治法的思想，所以在很多笔试面试中能经常看到快排的影子。可见掌握快排的重要性。  
从数列中挑出一个元素作为基准数。  
分区过程，将比基准数大的放到右边，小于或等于它的数都放到左边。  
再对左右区间递归执行第二步，直至各区间只有一个数。  
```python
# 10000个随机数据排序耗时0.05s  
def quick_sort(ary):  
    return qsort(ary, 0, len(ary) - 1)  

  
  def qsort(ary, left, right):  
    # 快排函数，ary为待排序数组，left为待排序的左边界，right为右边界  
    if left >= right: return ary  
    key = ary[left]  # 取最左边的为基准数  
    lp = left  # 左指针  
    rp = right  # 右指针  
    while lp < rp:  # 如果左指针在右指针右边就死循环  
        while ary[rp] >= key and lp < rp:  # 拿右指针上的值和key比较, 如果比key大,就向左移指针,直至条件不再成立  
            rp -= 1  
        while ary[lp] <= key and lp < rp:  
            lp += 1  
        ary[lp], ary[rp] = ary[rp], ary[lp]  # 对调左右指针上的值  
        # print(ary, 'key:%s lp:%s rp:%s' % (key, lp, rp))  
    ary[left], ary[lp] = ary[lp], ary[left]  # 由上条件知道此时左指针值比key小,对调,下次循环基准数更新  
    qsort(ary, left, lp - 1)  
    qsort(ary, rp + 1, right)  
    return ary  
```

### 堆排序 HeapSort  

  ![Heapsort-example.gif | center | 350x280](https://cdn.nlark.com/yuque/0/2018/gif/178857/1537450449821-e61ddc56-93b3-4227-846f-3c1db8ec36d3.gif "")  
  
堆排序在 top K 问题中使用比较频繁。堆排序是采用二叉堆的数据结构来实现的，虽然实质上还是一维数组。二叉堆是一个近似完全二叉树 。  
二叉堆具有以下特性：  
父节点的键值总是大于或等于（小于或等于）任何一个子节点的键值。  
每个节点的左右子树都是一个二叉堆（都是最大堆或最小堆）。  
步骤：  
构造最大堆（Build\_Max\_Heap）：若数组下标范围为0~n，考虑到单独一个元素是大根堆，则从下标n/2开始的元素均为大根堆。于是只要从n/2-1开始，向前依次构造大根堆，这样就能保证，构造到某个节点时，它的左右子树都已经是大根堆。  
堆排序（HeapSort）：由于堆是用数组模拟的。得到一个大根堆后，数组内部并不是有序的。因此需要将堆化数组有序化。思想是移除根节点，并做最大堆调整的递归运算。第一次将heap[0]与heap[n-1]交换，再对heap[0...n-2]做最大堆调整。第二次将heap[0]与heap[n-2]交换，再对heap[0...n-3]做最大堆调整。重复该操作直至heap[0]和heap[1]交换。由于每次都是将最大的数并入到后面的有序区间，故操作完后整个数组就是有序的了。  
最大堆调整（Max\_Heapify）：该方法是提供给上述两个过程调用的。目的是将堆的末端子节点作调整，使得子节点永远小于父节点 。  
```python
# 堆排序 10000个随机数据排序耗时0.1s  
def heap_sort(ary):  
    n = len(ary)  
    first = int(n / 2 - 1)  # 最后一个非叶子节点  
    for start in range(first, -1, -1):  # 倒序遍历,构造大根堆, 整个数组内部子树都已经是大根堆,但并不是有序的  
        max_heapify(ary, start, n - 1)  
        print(ary)  
    for end in range(n - 1, 0, -1):  # 堆排，将大根堆转换成有序数组;思想是移除根节点，并做最大堆调整的递归运算。  每次循环调整边界-1  
        ary[end], ary[0] = ary[0], ary[end]  # 用最后一个元素和第一个元素对调  
        max_heapify(ary, 0, end - 1)  
        print(ary)  
    return ary  

  def max_heapify(ary, start, end):  
    """  
    子树(三个元素)最大堆调整：将堆的末端子节点作调整，使得子节点永远小于父节点  
    :param start: 为当前需要调整最大堆的位置  
    :param end: 调整边界  
    """  
    root = start  
    while True:  
        child = root * 2 + 1  # 调整节点的子节点  
        if child > end: break  
        if child + 1 <= end and ary[child] < ary[child + 1]:  
            child = child + 1  # 取较大的子节点  
        if ary[root] < ary[child]:  # 较大的子节点成为父节点  
            ary[root], ary[child] = ary[child], ary[root]  # 交换  
            root = child  
        else:  
            break  
```

### 二分查找  
```python
def binary_search(li,find):    
    low = 0    
    high = len(li)-1 # 需要减一否则会下标越界    
    while low <= high:    
        middle = (low + high) /2    
        if li[middle] ==  find :    
            return middle    
        elif li[middle] > find:    
            high = middle - 1    
        elif li[middle] < find:    
            low = middle + 1    
    return -1    
if __name__ == '__main__':    
    li = [x for x in range(1,101)]    
    for x in range(102):    
        print binary_search(li,x)   
```

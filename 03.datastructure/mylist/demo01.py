lis = [2,4,5,6,7]
for i in lis:
    if i % 2==0:
        lis.remove(i)
print(lis)
# [4, 5, 7]

# `for i in lis` 遍历**依赖列表下标**，一边遍历一边删元素，列表会自动前移，造成元素被跳过：
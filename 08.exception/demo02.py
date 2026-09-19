
# print(1/0)


try:
    print(1/0)
except ZeroDivisionError as e0:
    print('xxx')
    print(e0)
except Exception as e1:
    # 不会执行
    print(e1)
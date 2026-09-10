

# BaseException
# 下面有SystemExit/KeyboardInterrupt/GeneratorExit/Exception(其他异常都属于它)


class Exception1(Exception):
    pass

class Exception2(Exception):
    pass



try:
     # func   # 可能会抛出异常的代码
    print(1/0)
except (Exception1, Exception2) as e:  # 可以捕获多个异常并处理
    # 异常处理的代码
    print(e)
else:
    pass
    # pass  # 异常没有发生的时候代码逻辑
finally:
    pass     # 无论异常有没有发生都会执行的代码，一般处理资源的关闭和释放


# 继承Exception实现自定义异常，给异常加上一些附加信息
#
# 不用baseException是因为这样的话ctrl+c的keybord异常就用不了了

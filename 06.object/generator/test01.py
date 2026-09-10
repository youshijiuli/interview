import random


# - 生成器就是可以生成值的函数
# - 当一个函数里有了yield关键字就成了生成器
# - 生成器可以挂起执行并且保持当前执行的状态


def func():

    yield 1


if __name__ == '__main__':
    res = func()
    print(res)
    item = next(res)
    print(item)
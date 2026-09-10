import numpy as np
import pandas as pd


def func1(a, b=[]):
    a.append(1)
    b.append(1)
    print(a, b)


if __name__ == '__main__':
    a = [1, 2, 3]
    b = [4, 5, 6]
    func1(a)

    print(a)
    print(b)

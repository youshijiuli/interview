## Python

##### python 程序的输出有乱码，怎么解决

coding: utf-8

##### python 解释器执行程序时的过程

当 Python 程序运行时，编译的结果则是保存在内存中的 PyCodeObject 中，当 Python 程序运行结束时，Python 解释器则将 PyCodeObject 保留在 pyc 文件中。当 python 程序第二次执行时，首先程序会从硬盘中运行 pyc 文件，如果找到了则直接载入，否则就重复上面的过程。

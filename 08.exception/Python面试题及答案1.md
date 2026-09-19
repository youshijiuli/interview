### Python语言特性

#### 37 介绍一下except的用法和作用？
答：try…except…except…[else…][finally…]
执行try下的语句，如果引发异常，则执行过程会跳到except语句。对每个except分支顺序尝试执行，如果引发的异常与except中的异常组匹配，执行相应的语句。如果所有的except都不匹配，则异常会传递到下一个调用本代码的最高层try代码中。
try下的语句正常执行，则执行else块代码。如果发生异常，就不会执行
如果存在finally语句，最后总是会执行。

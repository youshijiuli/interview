"""
rlist, wlist, elist = select.select( [sys.stdin], [], [] )

print(sys.stdin.read())

select 方法的三个參数都是 list 类型。
分别代表读事件、写事件、错误事件，相同方法返回值也是三个 list，包括的是哪些事件（读、写、异常）满足了。

上面的样例，因为參数仅仅有一个事件 sys.stdin，表示仅仅关心标准输入事件，

因此当 select 返回时 rlist 仅仅会是 [sys.stdin]。
表示能够从 stdin 中读入数据了。
我们使用 read 方法来读入数据。

当然 select 对于 socket 描写叙述符也是有效的。
以下的一个样例是创建了两个 socket client连接到远程server。select 用来监控哪个 socket 有数据到达
"""
import socket
import select

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock1.connect(('127.0.0.1', 25))
sock2.connect(('127.0.0.1', 25))

while 1:

    # Await a read event
    rlist, wlist, elist = select.select([sock1, sock2], [], [], 5)

    # Test for timeout
    if [rlist, wlist, elist] == [[], [], []]:
        print("Five seconds elapsed.\n")

    else:
        # 遍历 rlist 中的每个套接字，读取并打印可用数据
        for sock in rlist:
            print(sock.recv(100))

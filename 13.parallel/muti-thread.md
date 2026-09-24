# muti\-thread

多线程编程在Python中使用`threading`模块来实现。以下是一些常见的多线程代码示例，包括线程的创建、启动、等待线程结束以及线程池的使用。

1. 创建并启动线程:

```Plain Text
**import** threading
**import** time

**def** **my_function**():**for** _ **in** range(5):
        print("Executing my_function")
        time.sleep(1)

*# 创建线程*
my_thread = threading.Thread(target=my_function)

*# 启动线程*
my_thread.start()

*# 主线程继续执行其他任务***for** _ **in** range(3):
    print("Executing main thread")
    time.sleep(1)

*# 等待线程结束*
my_thread.join()

print("Main thread and my_thread have finished.")
```

2. 使用`Thread`类的其他API:

```Plain Text
**import** threading

**def** **my_function**():
    print("Executing my_function")

*# 创建线程*
my_thread = threading.Thread(target=my_function)

*# 获取线程名称*
thread_name = my_thread.name
print("Thread Name:", thread_name)

*# 设置线程名称*
my_thread.name = "CustomThreadName"
print("Updated Thread Name:", my_thread.name)

*# 获取线程ID*
thread_id = my_thread.ident
print("Thread ID:", thread_id)
```

3. 使用线程池:

```Plain Text
**import** concurrent.futures
**import** requests

**def** **download_image**(url):
    response = requests.get(url)
    filename = url.split("/")[-1]
    **with** open(filename, "wb") **as** file:
        file.write(response.content)
    print(f"Downloaded {filename}")

*# 使用线程池***with** concurrent.futures.ThreadPoolExecutor() **as** executor:
    *# 提交多个任务到线程池*
    image_urls = ["url1", "url2", "url3"]
    executor.map(download_image, image_urls)
```

4. 多线程爬取图片案例:

```Plain Text
**import** threading
**import** requests

**def** **download_image**(url, filename):
    response = requests.get(url)
    **with** open(filename, "wb") **as** file:
        file.write(response.content)
    print(f"Downloaded {filename}")

*# 图片URL列表*
image_urls = ["url1", "url2", "url3"]

*# 创建并启动多个线程进行下载*
threads = []
**for** i, url **in** enumerate(image_urls, start=1):
    filename = f"image_{i}.jpg"
    thread = threading.Thread(target=download_image, args=(url, filename))
    threads.append(thread)
    thread.start()

*# 等待所有线程结束***for** thread **in** threads:
    thread.join()

print("All threads have finished downloading images.")
```

请注意，在多线程爬取图片的案例中，每个线程负责下载一个图片。你可以根据实际需求调整线程数和下载的图片URL。在使用多线程时，要注意线程安全性，确保多个线程之间不会发生竞争条件。

当涉及到多线程的应用场景时，有很多不同的情境，以下是一些常见的多线程应用场景，并附有详细的示例代码：

1. 并行下载多个文件:

```Plain Text
**import** threading
**import** requests

**def** **download_file**(url, filename):
    response = requests.get(url)
    **with** open(filename, "wb") **as** file:
        file.write(response.content)
    print(f"Downloaded {filename}")

*# 文件URL列表*
file_urls = ["url1", "url2", "url3"]

*# 创建并启动多个线程进行下载*
threads = []
**for** i, url **in** enumerate(file_urls, start=1):
    filename = f"file_{i}.txt"
    thread = threading.Thread(target=download_file, args=(url, filename))
    threads.append(thread)
    thread.start()

*# 等待所有线程结束***for** thread **in** threads:
    thread.join()

print("All threads have finished downloading files.")
```

2. 实现生产者\-消费者模型:

```Plain Text
**import** threading
**import** queue
**import** time

**def** **producer**(queue, data):**for** item **in** data:
        print(f"Producing {item}")
        queue.put(item)
        time.sleep(1)

**def** **consumer**(queue):**while** True:
        item = queue.get()
        **if** item **is** None:
            **break**
        print(f"Consuming {item}")
        time.sleep(2)

*# 创建队列*
my_queue = queue.Queue()

*# 创建并启动生产者和消费者线程*
producer_thread = threading.Thread(target=producer, args=(my_queue, ["item1", "item2", "item3"]))
consumer_thread = threading.Thread(target=consumer, args=(my_queue,))

producer_thread.start()
consumer_thread.start()

*# 等待生产者线程完成*
producer_thread.join()

*# 等待队列清空*
my_queue.join()

*# 发送终止信号给消费者线程*
my_queue.put(None)
consumer_thread.join()

print("Producer-consumer model has finished.")
```

3. 多线程处理数据集:

```Plain Text
**import** threading

**def** **process_data**(data_chunk):**for** item **in** data_chunk:
        *# 处理数据的逻辑*
        print(f"Processing {item}")

*# 模拟数据集*
data_set = ["data1", "data2", "data3", "data4", "data5"]

*# 切分数据集*
chunk_size = 2
data_chunks = [data_set[i:i+chunk_size] **for** i **in** range(0, len(data_set), chunk_size)]

*# 创建并启动多个线程处理数据*
threads = []
**for** i, data_chunk **in** enumerate(data_chunks, start=1):
    thread = threading.Thread(target=process_data, args=(data_chunk,))
    threads.append(thread)
    thread.start()

*# 等待所有线程结束***for** thread **in** threads:
    thread.join()

print("All threads have finished processing the data.")
```

4. 使用线程池执行并发任务:

```Plain Text
**import** concurrent.futures
**import** time

**def** **task_function**(task_id):
    print(f"Executing Task-{task_id}")
    time.sleep(2)
    **return** f"Task-{task_id} completed"*# 使用*
```

线程池执行并发任务的代码示例：

```Plain Text
**import** concurrent.futures

**def** **task_function**(task_id):
    print(f"Executing Task-{task_id}")
    *# 模拟任务执行***return** f"Task-{task_id} completed"*# 使用线程池***with** concurrent.futures.ThreadPoolExecutor(max_workers=3) **as** executor:
    *# 提交多个任务到线程池*
    task_ids = [1, 2, 3, 4, 5]
    futures = {executor.submit(task_function, task_id): task_id **for** task_id **in** task_ids}

    *# 获取任务执行结果***for** future **in** concurrent.futures.as_completed(futures):
        task_id = futures[future]
        **try**:
            result = future.result()
            print(f"Task-{task_id} result: {result}")
        **except** Exception **as** e:
            print(f"Task-{task_id} encountered an error: {e}")
```

这个例子演示了如何使用线程池执行多个并发任务，并获取它们的执行结果。你可以根据具体的需求调整线程池的`max_workers`参数，以及任务的具体实现逻辑。

以上是一些常见的多线程应用场景和相应的代码示例。多线程编程需要注意线程安全性和同步问题，确保多个线程之间正确协作。如果有其他具体用法或者更复杂的情况，欢迎提出，我将尽力为你提供帮助。

## features

`concurrent.futures` 是一个用于并发执行任务的 Python 模块，主要包含 `ThreadPoolExecutor` 和 `ProcessPoolExecutor` 两个类。以下是常见的使用方法和参数介绍：

### `ThreadPoolExecutor`:

1. 创建线程池：

```Plain Text
**from** concurrent.futures **import** ThreadPoolExecutor

**with** ThreadPoolExecutor(max_workers=5) **as** executor:
    *# Submit tasks for execution*
    future = executor.submit(some_function, arg1, arg2)
    *# Retrieve results*
    result = future.result()
```

1. 使用`map`方法批量提交任务：

```Plain Text
**from** concurrent.futures **import** ThreadPoolExecutor

**with** ThreadPoolExecutor(max_workers=5) **as** executor:
    results = executor.map(some_function, list_of_args)
    **for** result **in** results:
        *# Process results*
```

1. `submit`方法的超时设置：

```Plain Text
**from** concurrent.futures **import** ThreadPoolExecutor
**import** time

**with** ThreadPoolExecutor(max_workers=5) **as** executor:
    future = executor.submit(some_function, arg1, arg2)
    result = future.result(timeout=2)  *# Wait at most 2 seconds for the result*
```

### `ProcessPoolExecutor`:

1. 创建进程池：

```Plain Text
**from** concurrent.futures **import** ProcessPoolExecutor

**with** ProcessPoolExecutor(max_workers=3) **as** executor:
    *# Submit tasks for execution*
    future = executor.submit(some_function, arg1, arg2)
    *# Retrieve results*
    result = future.result()
```

1. 使用`map`方法批量提交任务：

```Plain Text
**from** concurrent.futures **import** ProcessPoolExecutor

**with** ProcessPoolExecutor(max_workers=3) **as** executor:
    results = executor.map(some_function, list_of_args)
    **for** result **in** results:
        *# Process results*
```

1. `submit`方法的超时设置：

```Plain Text
**from** concurrent.futures **import** ProcessPoolExecutor
**import** time

**with** ProcessPoolExecutor(max_workers=3) **as** executor:
    future = executor.submit(some_function, arg1, arg2)
    result = future.result(timeout=2)  *# Wait at most 2 seconds for the result*
```

这些方法可以帮助您在多线程或多进程情况下管理任务的执行。根据您的具体需求，您可以灵活使用这些API。

## subprocess

`subprocess` 模块用于创建和管理子进程，执行外部命令。以下是 `subprocess` 模块的一些常见用法和参数介绍：

### 创建子进程并执行命令：

```Plain Text
**import** subprocess

*# 执行命令，等待命令完成*
result = subprocess.run(["ls", "-l"], stdout=subprocess.PIPE, text=True)
print(result.stdout)

*# 使用check_call执行命令，检查返回码*
subprocess.check_call(["echo", "Hello, subprocess!"])

*# 使用check_output获取命令输出*
output = subprocess.check_output(["echo", "Hello, subprocess!"], text=True)
print(output)
```

### 控制子进程的输入和输出：

```Plain Text
**import** subprocess

*# 使用communicate方法与子进程进行交互*
process = subprocess.Popen(["grep", "pattern"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
output, _ = process.communicate(input="Some text to grep\nAnother line\n")

*# 将子进程的输出重定向到文件***with** open("output.txt", "w") **as** f:
    subprocess.run(["ls", "-l"], stdout=f)

*# 通过管道连接多个子进程*
p1 = subprocess.Popen(["cat", "file.txt"], stdout=subprocess.PIPE, text=True)
p2 = subprocess.Popen(["grep", "pattern"], stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
p1.stdout.close()  *# Allow p1 to receive a SIGPIPE if p2 exits.*
output, _ = p2.communicate()
print(output)
```

### 设置其他参数：

```Plain Text
**import** subprocess

*# 设置工作目录*
subprocess.run(["ls", "-l"], cwd="/path/to/directory")

*# 设置环境变量*
subprocess.run(["echo", "$HOME"], shell=True, env={"HOME": "/custom/home/path"})

*# 设置超时时间***try**:
    subprocess.run(["command"], timeout=5)
**except** subprocess.TimeoutExpired **as** e:
    print(f"Command timed out: {e}")

*# 捕获标准错误*
result = subprocess.run(["ls", "nonexistentfile"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(result.stderr)
```

这些是一些常见用法，具体的使用方法取决于您的具体需求和操作系统。希望这能帮助您更好地使用 `subprocess` 模块。





---



# 多线程

#### 1\.关于start和join两个API

当使用Python的多线程时，`t.start()`和`t.join()`是两个重要的函数，用于启动线程和等待线程执行完成。

1. t\.start\(\)

    - `t.start()`用于启动线程的执行。当你调用`t.start()`时，Python会创建一个新的线程，并在新线程中执行`run`方法中的代码。`run`方法是Thread类的一个默认方法，你可以通过继承Thread类并重写`run`方法来定义线程的执行逻辑。

    - 一旦你调用了`t.start()`，新线程就会开始执行，而不会阻塞当前线程。这意味着程序会继续执行后续代码，而不用等待新线程执行完成。

2. t\.join\(\)

    - `t.join()`用于等待线程执行完成。当你调用`t.join()`时，当前线程会被阻塞，直到线程t执行完成。这可以用来确保在主线程中需要等待子线程完成后再继续执行后续逻辑。

    - 通常来说，你会在主线程中创建并启动多个子线程，然后使用`t.join()`来等待所有子线程执行完成，然后再继续执行后续逻辑。

示例代码如下：

```Plain Text
**from** threading **import** Thread
**import** time

**def** **thread_function**(name):
    print(f"Thread {name} started")
    time.sleep(2)
    print(f"Thread {name} finished")

**if** __name__ == "__main__":
    t1 = Thread(target=thread_function, args=(1,))
    t2 = Thread(target=thread_function, args=(2,))
    
    t1.start()  *# 启动线程1*
    t2.start()  *# 启动线程2*
    
    t1.join()   *# 等待线程1执行完成*
    t2.join()   *# 等待线程2执行完成*
    
    print("All threads have finished")
```

在上面的示例中，我们创建了两个线程`t1`和`t2`，分别启动和等待它们的执行。这样可以确保在主线程中等待所有子线程执行完成后再继续执行后续逻辑。

希望这样的解释对你有所帮助。

#### 小示例

```Plain Text
**import** time
**import** random
**from** threading **import** Thread
**import** multiprocessing


**def** **task**(count, container: list):**for** _ **in** range(count):
        container.append(random.random())


**if** __name__ == '__main__':
    *# 1.基于循环# start = time.time()# count = 10000000# times = 10# alist = []# for i in range(times):#     task(count, alist)## end = time.time()# print('List processing completed!')# print(end - start) # 23.92203688621521# 2. 基于线程# start = time.time()# count = 10000000# times = 10# alist = []# jobs = []# for i in range(times):#     thread = Thread(target=task, args=(count, alist))#     jobs.append(thread)## for job in jobs:#     job.start()## for job in jobs:#     job.join()## end = time.time()# print('List processing completed!')# print(end - start)  # 23.898953914642334# 3.基于进程*
    start_time = time.time()
    size = 10000000
    procs = 10  *# 创建进程数，也是要执行的次数*
    jobs = []
    **for** i **in** range(procs):  *# 创建进程*
        out_list = []
        process = multiprocessing.Process(target=task, args=(size, out_list))
        jobs.append(process)
    **for** j **in** jobs:  *# 一个一个的进程开始执行*
        j.start()
    **for** j **in** jobs:  *# 一个一个的进程关闭*
        j.join()
    end_time = time.time()
    print('List processing completed!')
    print('multiprocessing time=', end_time - start_time) *# 17.122254848480225*
```

当我们比较基于循环、线程和进程的执行时间时，可以得到以下解释：

1. 基于循环的执行时间最长。因为在这种情况下，所有的任务都是在同一个线程中执行的，没有任何并行处理。因此，每次执行 `task` 函数时，都需要等待上一次执行结束后才能开始下一次的执行，这导致了总体执行时间较长。

2. 基于线程的执行时间接近基于循环的执行时间。由于 Python 的全局解释器锁（GIL），多线程无法实现真正的并行处理，因此所有的线程仍然在同一个 CPU 核心上轮流执行。虽然线程可以在 I/O 阻塞的情况下提高效率，但在 CPU 密集型任务中并不能实现真正的并行处理，因此执行时间与基于循环的方式相差不大。

3. 基于进程的执行时间最短。使用多进程可以充分利用多核 CPU 的优势，在多个进程之间实现真正的并行处理。每个进程都有自己独立的内存空间和 Python 解释器，因此可以同时执行多个任务。这使得基于进程的执行时间明显缩短，尤其是在 CPU 密集型任务中。

总的来说，在 CPU 密集型任务中，基于进程的并行处理效果最好，而基于线程的效果受到 GIL 的限制，无法充分利用多核 CPU 的优势。基于循环的方式由于串行执行，执行时间最长。


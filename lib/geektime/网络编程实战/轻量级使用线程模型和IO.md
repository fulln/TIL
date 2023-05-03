---
dg-publish: true
title: 轻量级使用线程模型和IO
createTime: 2023-05-03 21:26  
---

# 26 | 使用阻塞I/O和线程模型：换一种轻量的方式

我们使用了进程模型来处理用户连接请求，进程切换上下文的代价是比较高的，幸运的是，有一种轻量级的模型可以处理多用户连接请求，这就是线程模型。

现代操作系统都允许在单进程中运行多个线程。线程由操作系统内核管理。每个线程都有自己的上下文（context），包括一个可以唯一标识线程的 ID（thread ID，或者叫 tid）、栈、程序计数器、寄存器等。在同一个进程中，所有的线程共享该进程的整个虚拟地址空间，包括代码、数据、堆、共享库等。

#### 既然可以使用多进程来处理并发，为什么还要使用多线程模型呢？

在同一个进程下，线程上下文切换的开销要比进程小得多。怎么理解线程上下文呢？我们的代码被 CPU 执行的时候，是需要一些数据支撑的，比如程序计数器告诉 CPU 代码执行到哪里了，寄存器里存了当前计算的一些中间值，内存里放置了一些当前用到的变量等，从一个计算场景，切换到另外一个计算场景，程序计数器、寄存器等这些值重新载入新场景的值，就是线程的上下文切换。

### POSIX 线程模型

POSIX 线程是现代 UNIX 系统提供的处理线程的标准接口。POSIX 定义的线程函数大约有 60 多个，这些函数可以帮助我们创建线程、回收线程。接下来我们先看一个简单的例子程序。

```c

int another_shared = 0;

void thread_run(void *arg) {
    int *calculator = (int *) arg;
    printf("hello, world, tid == %d \n", pthread_self());
    for (int i = 0; i < 1000; i++) {
        *calculator += 1;
        another_shared += 1;
    }
}

int main(int c, char **v) {
    int calculator;

    pthread_t tid1;
    pthread_t tid2;

    pthread_create(&tid1, NULL, thread_run, &calculator);
    pthread_create(&tid2, NULL, thread_run, &calculator);

    pthread_join(tid1, NULL);
    pthread_join(tid2, NULL);

    printf("calculator is %d \n", calculator);
    printf("another_shared is %d \n", another_shared);
}
```

#### 构建线程池处理多个连接

如果并发连接过多，就会引起线程的频繁创建和销毁。虽然线程切换的上下文开销不大，但是线程创建和销毁的开销却是不小的。

可以使用预创建线程池的方式来进行优化。在服务器端启动时，可以先按照固定大小预创建出多个线程，当有新连接建立时，往连接字队列里放置这个新连接描述字，线程池里的线程负责从连接字队列里取出连接描述字进行处理

![](https://static001.geekbang.org/resource/image/d9/72/d976c7b993862f0dbef75354d2f49672.png?wh=1430*462)

这个程序的关键是连接字队列的设计，因为这里既有往这个队列里放置描述符的操作，也有从这个队列里取出描述符的操作。

一个是锁 mutex，一个是条件变量 condition。锁很好理解，加锁的意思就是其他线程不能进入；条件变量则是在多个线程需要交互的情况下，用来线程间同步的原语。

### 总结


# 地址

此文章为5月day3 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/145464》

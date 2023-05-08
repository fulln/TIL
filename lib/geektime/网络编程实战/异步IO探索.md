---
dg-publish: true
title: 异步IO探索
createTime: 2023-05-08 22:43  
---
# 30 | 真正的大杀器：异步I/O探索

### 阻塞 / 非阻塞 VS 同步 / 异步

#### 阻塞 I/O 

发起的 read 请求，线程会被挂起，一直等到内核数据准备好，并把数据从内核区域拷贝到应用程序的缓冲区中，当拷贝过程完成，read 请求调用才返回。接下来，应用程序就可以对缓冲区的数据进行数据解析

![](https://static001.geekbang.org/resource/image/e7/9a/e7f477d5c2e902de5a23b0e90cf9339a.png?wh=730*480)

#### 非阻塞 I/O

非阻塞的 read 请求在数据未准备好的情况下立即返回，应用程序可以不断轮询内核，直到数据准备好，内核将数据拷贝到应用程序缓冲，并完成这次 read 调用。注意，这里最后一次 read 调用，获取数据的过程，是一个同步的过程。这里的同步指的是内核区域的数据拷贝到缓冲区的这个过程。
![](https://static001.geekbang.org/resource/image/4f/0c/4f93d6e13fb78be2a937f962175c5b0c.png?wh=718*602)

#### select、poll 这样的 I/O 多路复用技术
当内核数据准备好时，再通知应用程序进行操作。这个做法大大改善了应用进程对 CPU 的利用率，在没有被通知的情况下，应用进程可以使用 CPU 做其他的事情。

![](https://static001.geekbang.org/resource/image/ea/dc/ea8552f28b0b630af702a9e7434f03dc.png?wh=756*446)


**同步调用、异步调用的说法，是对于获取数据的过程而言的，前面几种最后获取数据的 read 操作调用，都是同步的，在 read 调用时，内核将数据从内核空间拷贝到应用程序空间，这个过程是在 read 函数中同步进行的，如果内核实现的拷贝效率很差，read 调用就会在这个同步过程中消耗比较长的时间。**

#### AIO

当我们发起 aio_read 之后，就立即返回，内核自动将数据从内核空间拷贝到应用程序空间，这个拷贝过程是异步的，内核自动完成的，和前面的同步操作不一样，应用程序并不需要主动发起拷贝动作。

![](https://static001.geekbang.org/resource/image/de/71/de97e727087775971f83c70c38d6f771.png?wh=732*462)

### Linux 下 socket 套接字的异步支持

Linux 下对异步操作的支持非常有限，这也是为什么使用 epoll 等多路分发技术加上非阻塞 I/O 来解决 Linux 下高并发高性能网络 I/O 问题的根本原因

### Windows 下的 IOCP 和 Proactor 模式

和 Reactor 模式一样，Proactor 模式也存在一个无限循环运行的 event loop 线程，但是不同于 Reactor 模式，这个线程并不负责处理 I/O 调用，它只是负责在对应的 read、write 操作完成的情况下，分发完成事件到不同的处理函数。

由于系统内核提供了真正的“异步”操作，Proactor 不会再像 Reactor 一样，每次感知事件后再调用 read、write 方法完成数据的读写，它只负责感知事件完成，并由对应的 handler 发起异步读写请求，I/O 读写操作本身是由系统内核完成的。

**Reactor 模式是基于待完成的 I/O 事件，而 Proactor 模式则是基于已完成的 I/O 事件，**


# 地址

此文章为5月day8 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/150780》

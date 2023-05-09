---
dg-publish: true
title: # epoll源码深度剖析
createTime: 2023-05-09 23:30  
---
# 31丨性能篇答疑：epoll源码深度剖析

### 基本数据结构

epoll 中使用的数据结构，分别是 eventpoll、epitem 和 eppoll_entry。

### 总结

epoll 维护了一棵红黑树来跟踪所有待检测的文件描述字，黑红树的使用减少了内核和用户空间大量的数据拷贝和内存分配，大大提高了性能。

同时，epoll 维护了一个链表来记录就绪事件，内核在每个文件有事件发生时将自己登记到这个就绪事件列表中，通过内核自身的文件 file-eventpoll 之间的回调和唤醒机制，减少了对内核描述字的遍历，大大加速了事件通知和检测的效率，这也为 level-triggered 和 edge-triggered 的实现带来了便利。
# 32 | 自己动手写高性能HTTP服务器（一）：设计和思路

先要构建一个支持 TCP 的高性能网络编程框架，完成这个 TCP 高性能网络框架之后，再增加 HTTP 特性的支持就比较容易了，这样就可以很快开发出一个高性能的 HTTP 服务器程序。

### 设计需求

1. 第一，采用 reactor 模型，可以灵活使用 poll/epoll 作为事件分发实现。
2. 第二，必须支持多线程，从而可以支持单线程单 reactor 模式，也可以支持多线程主 - 从 reactor 模式。可以将套接字上的 I/O 事件分离到多个线程上。
3. 封装读写操作到 Buffer 对象中。

### 主要设计思路

#### 反应器模式设计

按照性能篇的讲解，主要是设计一个基于事件分发和回调的反应器框架。这个框架里面的主要对象包括：

1. event_loop
可以把 event_loop 这个对象理解成和一个线程绑定的无限事件循环，你会在各种语言里看到 event_loop 这个抽象。这是什么意思呢？简单来说，它就是一个无限循环着的事件分发器，一旦有事件发生，它就会回调预先定义好的回调函数，完成事件的处理。

2. channel
对各种注册到 event_loop 上的对象，我们抽象成 channel 来表示，例如注册到 event_loop 上的监听事件，注册到 event_loop 上的套接字读写事件等。在各种语言的 API 里，你都会看到 channel 这个对象，大体上它们表达的意思跟我们这里的设计思路是比较一致的。

3. acceptor
acceptor 对象表示的是服务器端监听器，acceptor 对象最终会作为一个 channel 对象，注册到 event_loop 上，以便进行连接完成的事件分发和检测。

4. event_dispatcher

event_dispatcher 是对事件分发机制的一种抽象，也就是说，可以实现一个基于 poll 的 poll_dispatcher，也可以实现一个基于 epoll 的 epoll_dispatcher。在这里，我们统一设计一个 event_dispatcher 结构体，来抽象这些行为。

1. channel_map

channel_map 保存了描述字到 channel 的映射，这样就可以在事件发生时，根据事件类型对应的套接字快速找到 channel 对象里的事件处理函数。

### I/O 模型和多线程模型设计

#### thread_pool

thread_pool 维护了一个 sub-reactor 的线程列表，它可以提供给主 reactor 线程使用，每次当有新的连接建立时，可以从 thread_pool 里获取一个线程，以便用它来完成对新连接套接字的 read/write 事件注册，将 I/O 线程和主 reactor 线程分离。

#### event_loop_thread

event_loop_thread 是 reactor 的线程实现，连接套接字的 read/write 事件检测都是在这个线程里完成的。

### Buffer 和数据读写

#### buffer

buffer 对象屏蔽了对套接字进行的写和读的操作，如果没有 buffer 对象，连接套接字的 read/write 事件都需要和字节流直接打交道，这显然是不友好的。所以，我们也提供了一个基本的 buffer 对象，用来表示从连接套接字收取的数据，以及应用程序即将需要发送出去的数据。

#### tcp_connection

tcp_connection 这个对象描述的是已建立的 TCP 连接。它的属性包括接收缓冲区、发送缓冲区、channel 对象等。这些都是一个 TCP 连接的天然属性。

tcp_connection 是大部分应用程序和我们的高性能框架直接打交道的数据结构。我们不想把最下层的 channel 对象暴露给应用程序，因为抽象的 channel 对象不仅仅可以表示 tcp_connection，前面提到的监听套接字也是一个 channel 对象，后面提到的唤醒 socketpair 也是一个 channel 对象。所以，我们设计了 tcp_connection 这个对象，希望可以提供给用户比较清晰的编程入口。


### 反应器模式设计

![](https://static001.geekbang.org/resource/image/7a/61/7ab9f89544aba2021a9d2ceb94ad9661.jpg?wh=3499*1264)

当 event_loop_run 完成之后，线程进入循环，首先执行 dispatch 事件分发，一旦有事件发生，就会调用 channel_event_activate 函数，在这个函数中完成事件回调函数 eventReadcallback 和 eventWritecallback 的调用，最后再进行 event_loop_handle_pending_channel，用来修改当前监听的事件列表，完成这个部分之后，又进入了事件分发循环。


# 地址

此文章为5月day9 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/152137》
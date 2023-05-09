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




# 地址

此文章为5月day9 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/152137》
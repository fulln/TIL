---
dg-publish: true
title: 动手写高性能HTTP服务器（二）
createTime: 2023-05-10 21:50  
---

# 33 | 自己动手写高性能HTTP服务器（二）：I/O模型和多线程模型实现

### 多线程设计的几个考虑

main reactor 线程是一个 acceptor 线程，这个线程一旦创建，会以 event_loop 形式阻塞在 event_dispatcher 的 dispatch 方法上，实际上，它在等待监听套接字上的事件发生，也就是已完成的连接，一旦有连接完成，就会创建出连接对象 tcp_connection，以及 channel 对象等。

当用户期望使用多个 sub-reactor 子线程时，主线程会创建多个子线程，每个子线程在创建之后，按照主线程指定的启动函数立即运行，并进行初始化。

#### 主线程如何判断子线程已经完成初始化并启动，继续执行下去呢？这是一个需要解决的重点问题。

将新创建的已连接套接字对应的读写事件交给一个 sub-reactor 线程处理。所以，这里从 thread_pool 中取出一个线程，通知这个线程有新的事件加入。而这个线程很可能是处于事件分发的阻塞调用之中，如何协调主线程数据写入给子线程，这是另一个需要解决的重点问题。

![](https://static001.geekbang.org/resource/image/55/14/55bb7ef8659395e39395b109dbd28f14.png?wh=1122*968)

### 主线程等待多个 sub-reactor 子线程初始化完
主线程需要等待子线程完成初始化，也就是需要获取子线程对应数据的反馈，而子线程初始化也是对这部分数据进行初始化，实际上这是一个多线程的通知问题。采用的做法在前面讲多线程的时候也提到过，使用 mutex 和 condition 两个主要武器。

#### 如果进入第二个循环，等待第二个子线程完成初始化，而此时第二个子线程已经初始化完成了，该怎么办？
注意我们这里一上来是加锁的，只要取得了这把锁，同时发现 event_loop_thread 的 eventLoop 对象已经变成非 NULL 值，可以肯定第二个线程已经初始化，就直接释放锁往下执行了。

#### 在执行 pthread_cond_wait 的时候，需要持有那把锁么？
父线程在调用 pthread_cond_wait 函数之后，会立即进入睡眠，并释放持有的那把互斥锁。而当父线程再从 pthread_cond_wait 返回时（这是子线程通过 pthread_cond_signal 通知达成的），该线程再次持有那把锁。

### 增加已连接套接字事件到 sub-reactor 线程中

主线程是一个 main reactor 线程，这个线程负责检测监听套接字上的事件，当有事件发生时，也就是一个连接已完成建立，如果我们有多个 sub-reactor 子线程，我们期望的结果是，把这个已连接套接字相关的 I/O 事件交给 sub-reactor 子线程负责检测。这样的好处是，main reactor 只负责连接套接字的建立，可以一直维持在一个非常高的处理效率，在多核的情况下，多个 sub-reactor 可以很好地利用上多核处理的优势。

sub-reactor 线程是一个无限循环的 event loop 执行体，在没有已注册事件发生的情况下，这个线程阻塞在 event_dispatcher 的 dispatch 上。你可以简单地认为阻塞在 poll 调用或者 epoll_wait 上，

####  主线程如何能把已连接套接字交给 sub-reactor 子线程呢？

如果我们能让 sub-reactor 线程从 event_dispatcher 的 dispatch 上返回，再让 sub-reactor 线程返回之后能够把新的已连接套接字事件注册上，这件事情就算完成了。

构建一个类似管道一样的描述字，让 event_dispatcher 注册该管道描述字，当我们想让 sub-reactor 线程苏醒时，往管道上发送一个字符就可以了。

调用了 socketpair 函数创建了套接字对，这个套接字对的作用就是我刚刚说过的，往这个套接字的一端写时，另外一端就可以感知到读的事件。其实，这里也可以直接使用 UNIX 上的 pipe 管道，作用是一样的。

#### 如果有新的连接产生，主线程是怎么操作的？

在 handle_connection_established 中，通过 accept 调用获取了已连接套接字，将其设置为非阻塞套接字（切记），接下来调用 thread_pool_get_loop 获取一个 event_loop。

调用 tcp_connection_new 创建 tcp_connection 对象的代码里，可以看到先是创建了一个 channel 对象，并注册了 READ 事件，之后调用 event_loop_add_channel_event 方法往子线程中增加 channel 对象。

如果能够获取锁，主线程就会调用 event_loop_channel_buffer_nolock 往子线程的数据中增加需要处理的 channel event 对象。所有增加的 channel 对象以列表的形式维护在子线程的数据结构中。

如果当前增加 channel event 的不是当前 event loop 线程自己，就会调用 event_loop_wakeup 函数把 event_loop 子线程唤醒。






# 地址

此文章为5月day10 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/154597》

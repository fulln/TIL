---
dg-publish: true
title: kafka请求是怎么被处理的
createTime: 2023-06-30 23:43  
---

Apache Kafka 自己定义了一组请求协议，用于实现各种各样的交互操作。比如常见的 PRODUCE 请求是用于生产消息的，FETCH 请求是用于消费消息的，METADATA 请求是用于请求 Kafka 集群元数据信息的。


## TCP

所有的请求都是通过 TCP 网络以 Socket 的方式进行通讯的。

1. 顺序处理请求
2. 每个请求使用单独线程处理。

Kafka 使用的是 Reactor 模式。

### Reactor 模型

Reactor 模式是事件驱动架构的一种实现方式，特别适合应用于处理多个客户端并发向服务器端发送请求的场景

![](https://static001.geekbang.org/resource/image/5b/3c/5bf8e3e8d35d1ac62yydb092700b683c.jpg?wh=3770*1801)

Kafka 的 Broker 端有个 SocketServer 组件，类似于 Reactor 模式中的 Dispatcher，它也有对应的 Acceptor 线程和一个工作线程池，只不过在 Kafka 中，这个工作线程池有个专属的名字，叫网络线程池。


### 异步线程处理

客户端发来的请求会被 Broker 端的 Acceptor 线程分发到任意一个网络线程中，由它们来进行处理。那么，当网络线程接收到请求后，它是怎么处理的呢？你可能会认为，它顺序处理不就好了吗？实际上，Kafka 在这个环节又做了一层异步线程池的处理

![](https://static001.geekbang.org/resource/image/41/95/41e0a69ed649f9c5yyea390edcd79a95.jpg?wh=3537*2088)

它不是自己处理，而是将请求放入到一个共享请求队列中

Broker 端还有个 IO 线程池，负责从该队列中取出请求，执行真正的处理。如果是 PRODUCE 生产请求，则将消息写入到底层的磁盘日志中；如果是 FETCH 请求，则从磁盘或页缓存中读取消息。

Broker 端参数 num.io.threads 控制了这个线程池中的线程数。目前该参数默认值是 8，表示每台 Broker 启动后自动创建 8 个 IO 线程处理请求。


请求队列是所有网络线程共享的，而响应队列则是每个网络线程专属的，Dispatcher 只是用于请求分发而不负责响应回传，因此只能让每个网络线程自己发送 Response 给客户端，所以这些 Response 也就没必要放在一个公共的地方


### 缓存延时请求

所谓延时请求，就是那些一时未满足条件不能立刻处理的请求。比如设置了 acks=all 的 PRODUCE 请求，一旦设置了 acks=all，那么该请求就必须等待 ISR 中所有副本都接收了消息后才能返回，此时处理该请求的 IO 线程就必须等待其他 Broker 的写入结果。当请求不能立刻处理时，它就会暂存在 Purgatory 中。稍后一旦满足了完成条件，IO 线程会继续处理该请求，并将 Response 放入对应网络线程的响应队列中



# 地址

此文章为6月day30 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/110482》


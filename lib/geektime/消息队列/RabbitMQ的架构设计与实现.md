---
dg-publish: true
title: RabbitMQ的架构设计与实现
createTime: 2023-08-07 23:26  
---

# RabbitMQ的架构设计与实现

最基础的消息队列应该具备**通信协议、网络模块、存储模块、生产者、消费者**五个模块

### RabbitMQ 系统架构
![](https://static001.geekbang.org/resource/image/f8/8d/f87175e8b0e42c14bf648dfa8f18608d.jpg?wh=10666x5157)


RabbitMQ 由 Producer、Broker、Consumer 三个大模块组成。生产者将数据发送到 Broker，Broker 接收到数据后，将数据存储到对应的 Queue 里面，消费者从不同的 Queue 消费数据。

它还有 Exchange、Bind、Route 这几个独有的概念
-  Exchange
它是一个逻辑上的概念，用来做分发，本身不存储数据。流程上生产者先将消息发送到 Exchange，而不是发送到数据的实际存储单元 Queue 里面
-  Bind
Exchange 会根据一定的规则将数据分发到实际的 Queue 里面存储。这个分发过程就是 Route（路由）
-  Route
Exchange 会接收客户端发送过来的 route_key，然后根据不同的路由规则，将数据发送到不同的 Queue 里面。

**在 RabbitMQ 中是没有 Topic 这个用来组织分区的逻辑概念的。**

#### 协议和网络模块

RabbitMQ 在协议内容和连接管理方面，都是遵循 AMQP 规范。即 RabbitMQ 的模型架构和 AMQP 的模型架构是一样的，交换器、交换器类型、队列、绑定、路由键等都是遵循 AMQP 协议中相应的概念。

Connection 是指 TCP 连接，Channel 是 Connection 中的虚拟连接。两者的关系是：一个客户端和一个 Broker 之间只会建立一条 TCP 连接，就是指 Connection。Channel（虚拟连接）的概念在这个连接中定义，一个 Connection 中可以创建多个 Channel。

##### 客户端和服务端的实际通信都是在 Channel 维度通信的。
这个机制可以减少实际的 TCP 连接数量，从而降低网络模块的损耗。从设计角度看，也是基于 IO 复用、异步 I/O 的思路来设计的。
![](https://static001.geekbang.org/resource/image/82/62/821c6d165ab208520114b1aa4a922462.jpg?wh=10666x4972)
#### 数据存储
RabbitMQ 的存储模块也包含元数据存储与消息数据存储两部分。如下图所示，RabbitMQ 的两类数据都是存储在 Broker 节点上的，不会依赖第三方存储引擎。

#### 元数据存储

>RabbitMQ 的元数据都是存在于 Erlang 自带的分布式数据库 Mnesia 中的。即每台 Broker 都会起一个 Mnesia 进程，用来保存一份完整的元数据信息。因为 Mnesia 本身是一个分布式的数据库，自带了多节点的 Mnesia 数据库之间的同步机制。所以在元数据的存储模块，RabbitMQ 的 Broker 只需要调用本地的 Mnesia 接口保存、变更数据即可。不同节点的元数据同步 Mnesia 会自动完成。


# 地址

此文章为8月day7 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/674721》
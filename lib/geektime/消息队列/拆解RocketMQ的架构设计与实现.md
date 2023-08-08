---
dg-publish: true
title: 拆解RocketMQ的架构设计与实现
createTime: 2023-08-08 21:01  
---
# 拆解RocketMQ的架构设计与实现

### RocketMQ 系统架构
![](https://static001.geekbang.org/resource/image/6a/38/6af4ab5debc9535849ab7da3e5022f38.jpg?wh=10666x4161)

RocketMQ 由 **Producer、NameServer、Broker、Consumer** 四大模块组成。其中，NameServer 是 RocketMQ 的元数据存储组件。另外，在 RocketMQ 5.0 后，还增加了 Proxy 模块，用来支持 gRPC 协议，并为后续的计算存储分离架构做准备。

#### 从流程上看
>Broker 在启动的时候会先连接 NameServer，将各自的元数据信息上报给 NameServer，NameServer 会在内存中存储元数据信息。客户端在连接集群的时候，会配置对应的 NameServer 地址，通过连接 NameServer 来实现客户端寻址，从而连接上对应的 Broker。
>
>客户端在发送数据的时候，会指定 Topic 或 MessageQueue。Broker 收到数据后，将数据存储到对应的 Topic 中，消息存储在 Topic 的不同 Queue 中。在底层的文件存储中，所有 Queue 的数据是存储在同一个 CommitLog 文件中的。在订阅的时候会先创建对应的 Group，消费消息后，再确认数据。


### 协议和网络模块

![](https://static001.geekbang.org/resource/image/b1/c9/b1b45ffe1bf5e2870e53124815440dc9.jpg?wh=10666x4063)

在传输层协议方面，Remoting 和 gRPC 都是基于 TCP 协议传输的。Remoting 直接基于四层的 TCP 协议通信，gRPC 是基于七层的 HTTP2 协议通信，不过 HTTP2 底层也是基于 TCP，它们本质上都是应用层的协议。

**_Remoting 从功能、性能、灵活性来看没有太大的问题。它的主要缺点是私有协议客户端的重复开发成本，以及与第三方服务集成的不便捷。_**

#### GRPC架构
![](https://static001.geekbang.org/resource/image/b9/a3/b961c1a2a899610d7c0e0b5f24dcd0a3.png?wh=800x480)

gRPC 分为 Client 端和 Server 端，底层基于 HTTP2 通信，内置了编解码模块，也定义好了 Client 和 Server 之间的调用方式，同时支持 TLS 加密，是一个完整的 RPC 框架。所以我们可以看到它在底层已经实现了网络通信、协议的设计、编解码框架等所有基础的工作。

### 数据存储

数据存储模块也分为元数据存储和消息数据存储两部分。
#### 元数据存储

>RocketMQ 的元数据信息实际是存储在 Broker 上的，Broker 启动时将数据上报到 NameServer 模块中汇总缓存。NameServer 是一个简单的 TCP Server，专门用来接收、存储、分发 Broker 上报的元数据信息。这些元数据信息是存储在 NameServer 内存中的，NameServer 不会持久化去存储这些数据。

>Broker 启动或删除时，会调用 NameServer 的注册和退出接口，每个 Broker 都会存储自己节点所属的元数据信息（比如有哪些 Topic、哪些 Queue 在本节点上），在 Broker 启动时，会把全量的数据上报到 NameServer 中。

从部署形态上看，NameServer 是多节点部署的，是一个集群。 但是不同节点之间是没有相互通信的，所以本质上多个 NameServer 节点间数据没有一致性的概念，是各自维护自己的数据，由每台 Broker 上报元数据来维护每台 NameServer 节点上数据的准确性。

NameServer 不负责具体消息数据的存储和分发，所以在请求频率、负载方面都不会很高。所以在大多数场景下，NameServer 都是可以多集群共享的。从功能上看，它对 RocketMQ 的作用相当于 RabbitMQ 的 Mnesia。

### 消息数据
>RocketMQ 消息数据的最小存储单元是 MessageQueue，也就是我们常说的 Queue 或 Partition。Topic 可以包含一个或多个 MessageQueue，数据写入到 Topic 后，最终消息会分发到对应的 MessageQueue 中存储。

>在底层的文件存储方面，并不是一个 MessageQueue 对应一个文件存储的，而是一个节点对应一个总的存储文件，单个 Broker 节点下所有的队列共用一个日志数据文件（CommitLog）来存储，和 RabbitMQ 采用的是同一种存储结构。存储结构如下图所示：

![](https://static001.geekbang.org/resource/image/e5/69/e54d8fb1dffecbc91b978728b48a5369.png?wh=1142x763)


- CommitLog 是消息主体以及元数据存储主体，每个节点只有一个，客户端写入到所有 MessageQueue 的数据，最终都会存储到这一个文件中。

- ConsumeQueue 是逻辑消费队列，是消息消费的索引，不存储具体的消息数据。引入的目的主要是提高消息消费的性能。由于 RocketMQ 是基于主题 Topic 的订阅模式，消息消费是针对主题进行的，如果要遍历 Commitlog 文件，基于 Topic 检索消息是非常低效的。Consumer 可根据 ConsumeQueue 来查找待消费的消息，ConsumeQueue 文件可以看成是基于 Topic 的 CommitLog 索引文件。

- IndexFile 是索引文件，它在文件系统中是以 HashMap 结构存储的。在 RocketMQ 中，通过 Key 或时间区间来查询消息的功能就是由它实现的。

CommitLog 会存储所有的消息内容。所以为了保证数据的读写性能，我们会对 CommitLog 进行分段存储。CommitLog 底层默认单个文件大小为 1G，消息是顺序写入到文件中，当文件满了，就会写入下一个文件。对于 ConsumeQueue 和 IndexFile，则不需要分段存储，因为它们存储的是索引数据，数据量一般很小。

### 生产者与消费者

RocketMQ 的客户端连接服务端是需要经过客户端寻址的。如下图所示，首先和 NameServer 完成寻址，拿到 Topic/MessageQueue 和 Broker 的对应关系后，接下来才会和 Broker 进行交互。

#### 生产者

生产端的基础模块（如连接管理、心跳检测、协议构建、序列化等工作），则会以协议和网络层的设计为准，使用不同编程语言 SDK 完成对应的开发。例如，在 Java 中，我们可以使用 Netty 来构建客户端，进行 TCP 通信，根据 Remoting 协议构建请求数据，序列化后向服务端发起请求，或者直接使用 gRPC 框架的客户端进行通信。

生产者是将数据发送到 Topic 或者 Queue 里面的。如果是发送到 Topic，则数据要经历生产数据分区分配的过程。**即决定消息要发送到哪个目标分区**。

>RocketMQ 支持轮询算法和最小投递延迟算法两种策略。默认是轮询算法，该算法保证了每个 Queue 中可以均匀地获取到消息。最小投递延迟算法会统计每次消息投递的时间延迟，然后根据统计出的结果将消息投递到时间延迟最小的 Queue。如果是直接发送到 Queue，则无需经过分区选择，直接发送即可。


为了满足不同的发送场景，RocketMQ 支持**单向发送、同步发送、异步发送**三种发送形式。单向发送（Oneway）指发送消息后立即返回，不处理响应，不关心是否发送成功。同步发送（Sync）指发送消息后等待响应。异步发送（Async）指发送消息后立即返回，在提供的回调方法中处理响应。

#### 消费端
为了满足不同场景的消费需要，RocketMQ 同时支持 Pull、Push、Pop 三种消费模型。

>默认的消费模型是 Pull，Pull 的底层是以客户端会不断地去服务端拉取数据的形式实现的。Push 模型底层是以伪 Push 的方式实现的，即在客户端底层用一个 Pull 线程不断地去服务端拉取数据，拉到数据后，触发客户端设置的回调函数。让客户端从感受上看，是服务端直接将数据 Push 过来的。

RocketMQ 推出了 Pop 模式，将消费分区、分区分配关系、重平衡都移到了服务端，减少了重平衡机制给客户端带来的复杂性。

>RocketMQ 默认是通过消费分组机制来消费的。即在客户端消费数据的时候，会通过消费分组来管理消费关系和存储消费进度。从实现上看，同一条消息支持被多个消费分组订阅，每个消费者分组可以有多个消费者。

消费者负载均衡策略分为**消息粒度负载均衡和队列粒度负载均衡**两种模式。

1. 消息粒度负载均衡是指同一消费者分组内的多个消费者，将按照消息粒度平均分摊主题中的所有消息。即同一个队列中的消息，会被平均分配给多个消费者共同消费。
![](https://static001.geekbang.org/resource/image/bb/59/bb949f7cde7e5c710b7232b9978f3759.jpg?wh=10666x4626)
1. 队列粒度负载均衡是指同一消费者分组内的多个消费者，将按照队列粒度消费消息，即每个队列仅被一个消费者消费。
![](https://static001.geekbang.org/resource/image/27/be/278ceayydfbe148a7c7767497b5ccdbe.jpg?wh=10666x6000)

RocketMQ 通过提交消费位点信息来保存消费进度。在服务端，RocketMQ 会为每个消费分组维护一份消费位点信息，信息中会保存消费的最大位点、最小位点、当前消费位点等内容。
![](https://static001.geekbang.org/resource/image/db/42/db391cae3483d129fe5fc1d31eb2d242.jpg?wh=10666x4259)

客户端消费完数据后，就会调用 Broker 的消费位点更新接口，提交当前消费的位点信息。

>在服务端，消息被某个消费者消费完成后，不会立即在队列中被删除，以便当消费者客户端停止又再次重新上线时，会严格按照服务端保存的消费进度继续处理消息。如果服务端保存的历史位点信息已过期被删除，此时消费位点向前移动至服务端存储的最小位点。

### HTTP 协议支持和管控操作

RocketMQ 的管控也是不支持 HTTP 协议的操作的。RocketMQ 的管控操作都是通过 Remoting 协议支持的，在 gRPC 协议中也不支持管控操作。即在 Broker 中，通过 Remoting 协议暴露不同的接口或者在 NameServer 中暴露 TCP 的接口，来实现一些对应的管控操作。

## 总结RocketMQ

1. 协议层支持 Remoting 和 gRPC 两种协议。
2. 网络层是基于 Java NIO 框架 Netty 开发，底层也是通过多路复用、异步 IO、Reactor 模型等技术来提高网络模块的性能。
3. 存储层是基于多个 MessageQueue 的数据统一存储到一个文件的思路来设计的，同时也支持分段存储和基于时间的数据过期机制。
4. 元数据存储是使用 Broker + 自定义的 NameServer 之间的配合来实现的。
5. 客户端的访问需要经过客户端寻址机制，拿到元数据信息后，才直连 Broker。
6. 生产端是将数据写入到 Topic 或分区，写入 Topic 时需要经过生产分区分配操作，确认最终写入的 MessageQueue 也支持多种写入方式。
7. 消费端有消费分组的概念，也需要在多个消费者和消费分组之间进行消费的负载均衡，最后通过提交消费位点的形式来保存消费进度。

# 地址

此文章为8月day8 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/674914》
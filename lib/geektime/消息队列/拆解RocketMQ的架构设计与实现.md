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



# 地址

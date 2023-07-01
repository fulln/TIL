---
dg-publish: true
title: Consumer Rebalance
createTime: 2023-07-01 23:29  
---

## 消费者组重平衡全流程解析

重平衡需要借助 Kafka Broker 端的 Coordinator 组件，在 Coordinator 的帮助下完成整个消费者组的分区重分配


### rebalance的触发条件

1. 组成员数量的变化
2. topic数量的变化
3. 分区数的变化

**靠消费者端的心跳线程（Heartbeat Thread）通知其他消费者实例**

Kafka Java 消费者需要定期地发送心跳请求（Heartbeat Request）到 Broker 端的协调者，以表明它还存活着。
- 在 Kafka 0.10.1.0 版本之前，发送心跳请求是在消费者主线程完成的，也就是你写代码调用 KafkaConsumer.poll 方法的那个线程。
- 自 0.10.1.0 版本开始，社区引入了一个单独的心跳线程来专门执行心跳请求发送，避免了这个问题。

重平衡的通知机制正是通过心跳线程来完成的。当协调者决定开启新一轮重平衡后，它会将“REBALANCE_IN_PROGRESS”封装进心跳请求的响应中，发还给消费者实例。当消费者实例发现心跳响应中包含了“REBALANCE_IN_PROGRESS”，就能立马知道重平衡又开始了

### 消费者组状态机

这套状态机属于非常底层的设计，Kafka 官网上压根就没有提到过，但你最好还是了解一下，因为它能够帮助你搞懂消费者组的设计原理，比如消费者组的过期位移（Expired Offsets）删除等。

![](https://static001.geekbang.org/resource/image/3c/8b/3c281189cfb1d87173bc2d4b8149f38b.jpeg?wh=529*414)

**状态机的各个状态流转**

![](https://static001.geekbang.org/resource/image/a9/72/a97eb0e0ee2b97abaf2762b6e79d5b72.jpg?wh=3580*1505)

一个消费者组最开始是 Empty 状态，当重平衡过程开启后，它会被置于 PreparingRebalance 状态等待成员加入，之后变更到 CompletingRebalance 状态等待分配方案，最后流转到 Stable 状态完成重平衡。

Kafka 定期自动删除过期位移的条件就是，组要处于 Empty 状态。因此，如果你的消费者组停掉了很长时间（超过 7 天），那么 Kafka 很可能就把该组的位移数据删除

### 消费者端重平衡流程

1. JoinGroup
	1. 一旦收集了全部成员的 JoinGroup 请求后，协调者会从这些成员中选择一个担任这个消费者组的领导者。
	2. 第一个发送 JoinGroup 请求的成员自动成为领导者
2. SyncGroup


# 地址

此文章为7月day1 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/111226》


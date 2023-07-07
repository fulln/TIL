---
dg-publish: true
title: consumer 怎么管理tcp连接
createTime: 2023-06-28 23:42  
---

## consumer 何时创建TCP连接

#### TCP 连接是在调用 KafkaConsumer.poll 方法时被创建的

1. 发起 FindCoordinator 请求时。

需要向 Kafka 集群发送一个名为 FindCoordinator 的请求，希望 Kafka 集群告诉它哪个 Broker 是管理它的协调者。

消费者程序会向集群中当前负载最小的那台 Broker 发送请求。负载是如何评估的呢？其实很简单，就是看消费者连接的所有 Broker 中，谁的待发送请求最少

2. 连接协调者时。

消费者知晓了真正的协调者后，会创建连向该 Broker 的 Socket 连接。只有成功连入协调者，协调者才能开启正常的组协调操作，比如加入组、等待组分配方案、心跳请求处理、位移获取、位移提交等


3. 消费数据时

消费者会为每个要消费的分区创建与该分区领导者副本所在 Broker 连接的 TCP

## 创建多少个TCP 连接

只有连接了协调者，消费者进程才能正常地开启消费者组的各种功能以及后续的消息消费。


# 地址

此文章为6月day28 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/109121》
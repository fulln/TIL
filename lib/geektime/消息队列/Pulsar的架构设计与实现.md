---
dg-publish: true
title:  Pulsar的架构设计与实现
createTime: 2023-08-13 23:43  
---

# Pulsar的架构设计与实现

作为消息队列后起之秀的 Pulsar，因为其存算分离、多租户、多协议、丰富的产品特性、支持百万 Topic 等特点，逐渐为大家所熟知。从定位来看，Pulsar 希望同时满足消息和流的场景。从技术上来看，它当前主要对标的是 Kafka，解决 Kafka 在流场景中的一些技术缺陷，比如计算层弹性、超大分区支持等等。

### Pulsar 系统架构

![](https://static001.geekbang.org/resource/image/90/71/904fd20b6ced9af51ae9c25e1c196171.jpg?wh=10666x6000)

它和其他消息队列最大的区别在于 Pulsar 是基于计算存储分离的思想设计的架构，所以 Pulsar 整体架构要分为计算层和存储层两层。我们通常说的 Pulsar 是指计算层的 Broker 集群和存储层的 BookKeeper 集群两部分。
# 地址

此文章为8月day13 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/676532》
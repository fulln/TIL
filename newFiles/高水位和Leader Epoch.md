---
dg-publish: true
title: 未命名
createTime: 2023-07-13 23:35  
---

##   关于高水位和Leader Epoch的讨论

### 什么是高水位？

Kafka 的水位不是时间戳，更与时间无关。它是和位置信息绑定的，具体来说，它是用消息位移来表征的。另外，Kafka 源码使用的表述是高水位，因此，今天我也会统一使用“高水位”或它的缩写 HW 来进行讨论。值得注意的是，Kafka 中也有低水位（Low Watermark），它是与 Kafka 删除消息相关联的概念

### 高水位的作用

在 Kafka 中，高水位的作用主要有 2 个。

1. 定义消息可见性，即用来标识分区下的哪些消息是可以被消费者消费的。
2. 帮助 Kafka 完成副本同步。

![](https://static001.geekbang.org/resource/image/45/db/453ff803a31aa030feedba27aed17ddb.jpg?wh=4000*1583)

在分区高水位以下的消息被认为是已提交消息，反之就是未提交消息。消费者只能消费已提交消息

#### 不涉及kafka事务

这里我们不讨论 Kafka 事务，因为事务机制会影响消费者所能看到的消息的范围，它不只是简单依赖高水位来判断。它依靠一个名为 LSO（Log Stable Offset）的位移值来判断事务型消费者的可见性。



# 地址

此文章为7月day13 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/112118》
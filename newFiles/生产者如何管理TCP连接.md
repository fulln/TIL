---
dg-publish: true
title: 生产者如何管理TCP连接
createTime: 2023-06-25 20:57  
---

## 生产者如何管理TCP连接

## 为何采用TCP

1. 多路复用请求，即 multiplexing request，是指将两个或多个数据流合并到底层单一物理连接中的过程
2. 同时轮询多个连接

## 何时创建TCP连接

**1. 在创建 KafkaProducer 实例时，生产者应用会在后台创建并启动一个名为 Sender 的线程，该 Sender 线程开始运行时首先会创建与 Broker 的连接**

- 会连接 bootstrap.servers 参数指定的所有 Broker
	- 如果指定了多个broker连接信息，会创建多个broker的tcp连接
	- 任意一台都可以拿到整个集群的broker信息

> 在对象构造器中启动线程会造成 this 指针的逃逸。理论上，Sender 线程完全能够观测到一个尚未构造完成的 KafkaProducer 实例。当然，在构造对象时创建线程没有任何问题，但最好是不要同时启动它。

**2. 在更新元数据后可能**
**3. 在消息发送时可能**

1. 当 Producer 尝试给一个不存在的主题发送消息时，Broker 会告诉 Producer 说这个主题不存在。此时 Producer 会发送 METADATA 请求给 Kafka 集群，去尝试获取最新的元数据信息。
2. Producer 通过 metadata.max.age.ms 参数定期地去更新元数据信息

## 何时关闭TCP连接

1. 用户主动关闭
	1. 最推荐的方式还是调用 producer.close() 方法来关闭。
	2. kill -9
2. kafka自动关闭
	1. Producer 端参数 connections.max.idle.ms 的值有关。默认情况下该参数值是 9 分钟，即如果在 9 分钟内没有任何请求“流过”某个 TCP 连接，那么 Kafka 会主动帮你把该 TCP 连接关闭
		1. broker端被关闭的，tcp发起方是客户端，broker属于被动关闭的的场景，会导致产生大量的CLOSE_WAIT 连接
	2. 用户可以在 Producer 端设置 connections.max.idle.ms=-1 禁掉这种机制。一旦被设置成 -1，TCP 连接将成为永久长连接。当然这只是软件层面的“长连接”机制，由于 Kafka 创建的这些 Socket 连接都开启了 keepalive，因此 keepalive 探活机制还是会遵守的。
	
## 幂等性生产者
指定 Producer 幂等性的方法很简单，仅需要设置一个参数即可，即 props.put(“enable.idempotence”, ture)，或 props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG， true)

#### 作用范围

1. 只能保证单分区上的幂等性
2. 一个幂等性producer能保证某个topic的一个分区不出现重复消息，无法实现多个分区的幂等
3. 单会话的幂等性，重启后无效
4. 多会话上的幂等需要开启事务消息

## 事务型Producer

事务型 Producer 能够保证将消息原子性地写入到多个分区中。这批消息要么全部写入成功，要么全部失败。另外，事务型 Producer 也不惧进程的重启。Producer 重启回来后，Kafka 依然保证它们发送消息的精确一次处理。

### 开启方式

1. 和幂等性 Producer 一样，开启 enable.idempotence = true。
2. 设置 Producer 端参数 transactional. id。最好为其设置一个有意义的名字。

代码显示使用事务
```java
producer.initTransactions();
try {
            producer.beginTransaction();
            producer.send(record1);
            producer.send(record2);
            producer.commitTransaction();
} catch (KafkaException e) {
            producer.abortTransaction();
}
```


Record1 和 Record2 被当作一个事务统一提交到 Kafka，要么它们全部提交成功，要么全部写入失败

**实际上即使写入失败，Kafka 也会把它们写入到底层的日志中，也就是说 Consumer 还是会看到这些消息**

### Consumer端的改变处理

读取事务型 Producer 发送的消息也是需要一些变更的。修改起来也很简单，设置 isolation.level 参数的值即可。当前这个参数有两个取值：
1. read_uncommitted：这是默认值，表明 Consumer 能够读取到 Kafka 写入的任何消息，不论事务型 Producer 提交事务还是终止事务，其写入的消息都可以读取。很显然，如果你用了事务型 Producer，那么对应的 Consumer 就不要使用这个值。
2. read_committed：表明 Consumer 只会读取事务型 Producer 成功提交事务写入的消息。当然了，它也能看到非事务型 Producer 写入的所有消息。

# 地址

此文章为6月day25 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/222085》
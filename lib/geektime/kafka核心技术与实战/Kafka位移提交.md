---
dg-publish: true
title: Kafka位移提交
createTime: 2023-06-26 22:36  
---

## consumer offset

下一条消息的位移，而不是目前最新消费消息的位移。

Consumer 需要向 Kafka 汇报自己的位移数据，这个汇报过程被称为提交位移（Committing Offsets）。因为 Consumer 能够同时消费多个分区的数据，所以位移的提交实际上是在分区粒度上进行的，即 **Consumer 需要为分配给它的每个分区提交各自的位移数据。**

当 Consumer 发生故障重启之后，就能够从 Kafka 中读取之前提交的位移值

**consumer端角度看，位移提交分为同步提交和异步提交**

### 同步还是异步

Consumer 端有个参数 enable.auto.commit，把它设置为 true 或者压根不设置它就可以了。

#### 异步
KafkaConsumer#commitSync()。该方法会提交 KafkaConsumer#poll() 返回的最新位移

##### 自动提交

Kafka 会保证在开始调用 poll 方法时，提交上次 poll 返回的所有消息。从顺序上来说，poll 方法的逻辑是先提交上一批消息的位移，再处理下一批消息，因此它能保证不出现消费丢失的情况。但自动提交位移的一个问题在于，它可能会出现重复消费。

##### 手动提交

它的好处就在于更加灵活，你完全能够把控位移提交的时机和频率。但是，它也有一个缺陷，就是在调用 commitSync() 时，Consumer 程序会处于阻塞状态，直到远端的 Broker 返回提交结果，这个状态才会结束

**KafkaConsumer#commitAsync()。**

调用 commitAsync() 之后，它会立即返回，不会阻塞，因此不会影响 Consumer 应用的 TPS。由于它是异步的，Kafka 提供了回调函数（callback），供你实现提交之后的逻辑，比如记录日志或处理异常等。

commitAsync 的问题在于，出现问题时它不会自动重试。因为它是异步操作，倘若提交失败后自动重试，那么它重试时提交的位移值可能早已经“过期”或不是最新值了。因此，异步提交的重试其实没有意义，所以 commitAsync 是不会重试的。

##### offset提交

Kafka Consumer API 还提供了一组更为方便的方法，可以帮助你实现更精细化的位移管理功能。刚刚我们聊到的所有位移提交，都是提交 poll 方法返回的所有消息的位移，比如 poll 方法一次返回了 500 条消息，当你处理完这 500 条消息之后，前面我们提到的各种方法会一次性地将这 500 条消息的位移一并处理。简单来说，就是直接提交最新一条消息的位移。

Kafka Consumer API 为手动提交提供了这样的方法：commitSync(Map) 和 commitAsync(Map)。它们的参数是一个 Map 对象，键就是 TopicPartition，即消费的分区，而值是一个 OffsetAndMetadata 对象，保存的主要是位移数据。



# 地址 

此文章为6月day26 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/106904》
---
dg-publish: true
title: 当 Redis 生成 RDB 文件的时候，会怎么处理过期的 key？
createTime: 2023-11-15 10:15
tags:
  - redis
  - RDB
  - AOF
---
## 当 Redis 生成 RDB 文件的时候，会怎么处理过期的 key？

当 Redis生成RDB文件时，过期的key会被处理如下：

1. Redis会在生成RDB文件之前检查每个key的过期时间。
2. 如果一个key已经过期，Redis在生成RDB文件时不会包含该key的数据。
3. 过期的key在RDB文件中不会被加载到内存中。
4. 尽管过期的key在逻辑上不属于数据集，但它们仍然会在INFO命令和DBSIZE命令中被计算在内。
5. 当从RDB文件读取数据时，副本不会加载已过期的key。
6. 过期的key在副本和主实例中在逻辑上是相同的。

总结来说，Redis在生成RDB文件时会忽略已过期的key，这样可以减少RDB文件的大小并提高加载性能。

## 当 Redis 重写 AOF 文件的时候，会怎么处理过期的 key？

当 Redis 重写 AOF（Append-Only File）文件时，会对过期的键（key）进行处理。Redis 使用过期时间（expiration time）来管理键的生命周期。当键的过期时间到达时，Redis会自动将其标记为过期。

在AOF重写过程中，Redis会检查每个键的过期时间。如果一个键已经过期，Redis会在AOF文件中生成一个DEL命令，以便在重写后删除该键。这样可以确保AOF文件的内容与内存中的数据保持一致。

需要注意的是，AOF重写是一个后台操作，不会阻塞Redis服务器的正常运行。它会根据配置的规则和策略来决定何时进行重写操作。

总结起来，当Redis重写AOF文件时，会处理过期的键，确保AOF文件与内存中的数据保持一致，并在重写后删除过期的键。
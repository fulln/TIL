---
dg-publish: true
---
#java #redis #cache #集群 #极客时间 

# 16 | 用Redis构建缓存集群的最佳实践有哪些？

### Redis Cluster

#### 分片

1. 引入`slot` 概念，槽是 Redis 分片的基本单位，每个槽里面包含一些 Key。每个集群的槽数是固定的 16384（16 * 1024）个，每个 Key 落在哪个槽中也是固定的，计算方法是：
```c
HASH_SLOT = CRC16(key) mod 16384
```

先计算 Key 的 CRC 值，然后把这个 CRC 之后的 Key 值直接除以 16384，余数就是 Key 所在的槽。这个算法就是我们上节课讲过的哈希分片算法。

2. 将槽放置到具体redis节点

射关系保存在集群的每个 Redis 节点上，集群初始化的时候，Redis 会自动平均分配这 16384 个槽，也可以通过命令来调整。这个分槽的方法，也是我们上节课讲到过的分片算法：查表法。

3. 客户端连接任意节点访问数据

当客户端请求一个 Key 的时候，被请求的那个 Redis 实例先通过上面的公式，计算出这个 Key 在哪个槽中，然后再查询槽和节点的映射关系，找到数据所在的真正节点，如果这个节点正好是自己，那就直接执行命令返回结果。如果数据不在当前这个节点上，那就给客户端返回一个重定向的命令，告诉客户端，应该去连哪个节点上请求这个 Key 的数据。然后客户端会再连接正确的节点来访问。

4. 水平扩容

每次往集群增加节点的时候，需要从集群的那些老节点中，搬运一些槽到新节点，你可以手动指定哪些槽迁移到新节点上，也可以利用官方提供的[redis-trib.rb](http://download.redis.io/redis-stable/src/redis-trib.rb)脚本来自动重新分配槽，自动迁移

#### 分片优缺点

分片可以解决 Redis 保存海量数据的问题，并且客观上提升了 Redis 的并发能力和查询性能。但是并不能解决高可用的问题，每个节点都保存了整个集群数据的一个子集，任何一个节点宕机，都会导致这个宕机节点上的那部分数据无法访问。

### Redis Cluster 是怎么解决高可用问题

> [!INFO] 增加从节点，做主从复制

Redis Cluster 支持给每个分片增加一个或多个从节点，每个从节点在连接到主节点上之后，会先给主节点发送一个 SYNC 命令，请求一次全量复制，也就是把主节点上全部的数据都复制到从节点上。全量复制完成之后，进入同步阶段，主节点会把刚刚全量复制期间收到的命令，以及后续收到的命令持续地转发给从节点。


如果某个分片的主节点宕机了，集群中的其他节点会在这个分片的从节点中选出一个新的节点作为主节点继续提供服务。新的主节点选举出来后，集群中的所有节点都会感知到，这样，如果客户端的请求 Key 落在故障分片上，就会被重定向到新的主节点上。

### Redis Cluster 是如何应对高并发的

默认情况下，集群的读写请求都是由主节点负责的，从节点只是起一个热备的作用。当然了，Redis Cluster 也支持读写分离，在从节点上读取数据。

### 为什么 Redis Cluster 不适合超大规模集群？

Redis Cluster 的优点是易于使用。分片、主从复制、弹性扩容这些功能都可以做到自动化，通过简单的部署就可以获得一个大容量、高可靠、高可用的 Redis 集群，并且对于应用来说，近乎于是透明的。

**Redis Cluster 是非常适合构建中小规模 Redis 集群**，这里的中小规模指的是，大概几个到几十个节点这样规模的 Redis 集群。

**但是 Redis Cluster 不太适合构建超大规模集群，主要原因是，它采用了去中心化的设计**

> [!WARNING] Redis Cluster 采用了一种去中心化的流言 ([Gossip](https://en.wikipedia.org/wiki/Gossip_protocol)) 协议来传播集群配置的变化。

### 如何用 Redis 构建超大规模集群？

1. 一种是基于代理的方式，在客户端和 Redis 节点之间，还需要增加一层代理服务。这个代理服务有三个作用。
	1. 负责在客户端和 Redis 节点之间转发请求和响应。客户端只和代理服务打交道，代理收到客户端的请求之后，再转发到对应的 Redis 节点上，节点返回的响应再经由代理转发返回给客户端。
	2. 负责监控集群中所有 Redis 节点状态，如果发现有问题节点，及时进行主从切换。
	3. 维护集群的元数据，这个元数据主要就是集群所有节点的主从信息，以及槽和节点关系映射表
2. 把代理服务的寻址功能前移到客户端中去。客户端在发起请求之前，先去查询元数据，就可以知道要访问的是哪个分片和哪个节点，然后直连对应的 Redis 节点访问数据。
	![](https://static001.geekbang.org/resource/image/dc/da/dcaced0a9ce9842ef688c9626accdcda.jpg?wh=1142*605)

# 地址

此文章为3月day31 学习笔记，内容来源于[极客时间](https://time.geekbang.org/column/article/217590) 

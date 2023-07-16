---
dg-publish: true
title: Kafka动态配置
createTime: 2023-07-16 23:32  
---

## 动态配置

### 什么是动态 Broker 参数配置？

在 Kafka 安装目录的 config 路径下，有个 server.properties 文件。通常情况下，我们会指定这个文件的路径来启动 Broker。如果要设置 Broker 端的任何参数，我们必须在这个文件中显式地增加一行对应的配置，之后启动 Broker 进程，令参数生效。

#### Dynamic Update Mode

- read-only。被标记为 read-only 的参数和原来的参数行为一样，只有重启 Broker，才能令修改生效。
- per-broker。被标记为 per-broker 的参数属于动态参数，修改它之后，只会在对应的 Broker 上生效。
- cluster-wide。被标记为 cluster-wide 的参数也属于动态参数，修改它之后，会在整个集群范围内生效，也就是说，对所有 Broker 都生效。你也可以为具体的 Broker 修改 cluster-wide 参数。

### 使用场景

1. 动态调整 Broker 端各种线程池大小，实时应对突发流量。
2. 动态调整 Broker 端连接信息或安全配置信息。
3. 动态更新 SSL Keystore 有效期。
4. 动态调整 Broker 端 Compact 操作性能。
5. 实时变更 JMX 指标收集器 (JMX Metrics Reporter)。

### 保存配置

Kafka 将动态 Broker 参数保存在 ZooKeeper 中

changes 是用来实时监测动态参数变更的，不会保存参数值；topics 是用来保存 Kafka 主题级别参数的。虽然它们不属于动态 Broker 端参数，但其实它们也是能够动态变更的。

/config/brokers znode 才是真正保存动态 Broker 参数的地方。该 znode 下有两大类子节点。第一类子节点就只有一个，它有个固定的名字叫 < default >，保存的是前面说过的 cluster-wide 范围的动态参数；另一类则以 broker.id 为名，保存的是特定 Broker 的 per-broker 范围参数。由于是 per-broker 范围，因此这类子节点可能存在多个。

#### 可能改动的参数

1. log.retention.ms。
	修改日志留存时间
2.  num.io.threads  & num.network.threads。
	1. 动态 Broker 参数最实用的场景了。毕竟，在实际生产环境中，Broker 端请求处理能力经常要按需扩容
3. 与 SSL 相关的参数。
	1. 主要是 4 个参数（ssl.keystore.type、ssl.keystore.location、ssl.keystore.password 和 ssl.key.password）。允许动态实时调整它们之后，我们就能创建那些过期时间很短的 SSL 证书

# 地址

此文章为7月day16 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/113504》
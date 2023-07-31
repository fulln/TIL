---
dg-publish: true
title: Kafka认证机制
createTime: 2023-07-20 23:40  
---

# Kafka认证机制


**基于 SSL 的认证主要是指 Broker 和客户端的双路认证**（2-way authentication）。通常来说，SSL 加密（Encryption）已经启用了单向认证，即客户端认证 Broker 的证书（Certificate）。如果要做 SSL 认证，那么我们要启用双路认证，也就是说 Broker 也要认证客户端的证书。

### 认证机制的比较

使用 SSL 做信道加密的情况更多一些，但使用 SSL 实现认证不如使用 SASL。毕竟，SASL 能够支持你选择不同的实现机制，如 GSSAPI、SCRAM、PLAIN 等。因此，我的建议是你可以使用 SSL 来做通信加密，使用 SASL 来做 Kafka 的认证实现。


#### SASL 下又细分了很多种认证机制

1. GSSAPI 适用于本身已经做了 Kerberos 认证的场景，这样的话，SASL/GSSAPI 可以实现无缝集成。
2. PLAIN 在这里是一种认证机制，而 PLAINTEXT 说的是未使用 SSL 时的明文传输。

SASL/PLAIN 有这样一个弊端：它不能动态地增减认证用户，你必须重启 Kafka 集群才能令变更生效


SASL/SCRAM 就解决了这样的问题。它通过将认证用户信息保存在 ZooKeeper 的方式，避免了动态修改需要重启 Broker 的弊端。在实际使用过程中，你可以使用 Kafka 提供的命令动态地创建和删除用户，无需重启整个集群。因此，如果你打算使用 SASL/PLAIN，不妨改用 SASL/SCRAM 试试。不过要注意的是，后者是 0.10.2 版本引入的。你至少要升级到这个版本后才能使用。

3. SASL/SCRAM-SHA-256 配置实例

#### 第 1 步：创建用户
```shell
$ cd kafka_2.12-2.3.0/
$ bin/kafka-configs.sh --zookeeper localhost:2181 --alter --add-config 'SCRAM-SHA-256=[password=admin],SCRAM-SHA-512=[password=admin]' --entity-type users --entity-name admin
Completed Updating config for entity: user-principal 'admin'.
```

#### 第 2 步：创建 JAAS 文件

```
KafkaServer {
org.apache.kafka.common.security.scram.ScramLoginModule required
username="admin"
password="admin";
};
```

```shell 
sasl.enabled.mechanisms=SCRAM-SHA-256

sasl.mechanism.inter.broker.protocol=SCRAM-SHA-256

security.inter.broker.protocol=SASL_PLAINTEXT

listeners=SASL_PLAINTEXT://localhost:9092
```

#### 第 3 步：启动 Broker
```

$KAFKA_OPTS=-Djava.security.auth.login.config=<your_path>/kafka-broker.jaas bin/kafka-server-start.sh config/server1.properties
......
[2019-07-02 13:30:34,822] INFO Kafka commitId: fc1aaa116b661c8a (org.apache.kafka.common.utils.AppInfoParser)
[2019-07-02 13:30:34,822] INFO Kafka startTimeMs: 1562045434820 (org.apache.kafka.common.utils.AppInfoParser)
[2019-07-02 13:30:34,823] INFO [KafkaServer id=0] started (kafka.server.KafkaServer)
```
#### 第 4 步：发送消息
#### 第 5 步：消费消息
#### 第 6 步：动态增减用户
```shell

$ bin/kafka-configs.sh --zookeeper localhost:2181 --alter --delete-config 'SCRAM-SHA-256' --entity-type users --entity-name writer
Completed Updating config for entity: user-principal 'writer'.

$ bin/kafka-configs.sh --zookeeper localhost:2181 --alter --delete-config 'SCRAM-SHA-512' --entity-type users --entity-name writer
Completed Updating config for entity: user-principal 'writer'.

$ bin/kafka-configs.sh --zookeeper localhost:2181 --alter --add-config 'SCRAM-SHA-256=[iterations=8192,password=new_writer]' --entity-type users --entity-name new_writer
Completed Updating config for entity: user-principal 'new_writer'.

```


# 地址

此文章为7月day20 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/118347》
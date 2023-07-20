---
dg-publish: true
title: Kafka认证机制
createTime: 2023-07-20 23:40  
---

# Kafka认证机制


**基于 SSL 的认证主要是指 Broker 和客户端的双路认证**（2-way authentication）。通常来说，SSL 加密（Encryption）已经启用了单向认证，即客户端认证 Broker 的证书（Certificate）。如果要做 SSL 认证，那么我们要启用双路认证，也就是说 Broker 也要认证客户端的证书。

### 认证机制的比较

使用 SSL 做信道加密的情况更多一些，但使用 SSL 实现认证不如使用 SASL。毕竟，SASL 能够支持你选择不同的实现机制，如 GSSAPI、SCRAM、PLAIN 等。因此，我的建议是你可以使用 SSL 来做通信加密，使用 SASL 来做 Kafka 的认证实现。






# 地址

此文章为7月day20 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/118347》
---
dg-publish: true
title: RabbitMQ的架构设计与实现
createTime: 2023-08-07 23:26  
---

# RabbitMQ的架构设计与实现

最基础的消息队列应该具备**通信协议、网络模块、存储模块、生产者、消费者**五个模块

### RabbitMQ 系统架构
![](https://static001.geekbang.org/resource/image/f8/8d/f87175e8b0e42c14bf648dfa8f18608d.jpg?wh=10666x5157)


RabbitMQ 由 Producer、Broker、Consumer 三个大模块组成。生产者将数据发送到 Broker，Broker 接收到数据后，将数据存储到对应的 Queue 里面，消费者从不同的 Queue 消费数据。


# 地址

此文章为8月day7 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/674721》
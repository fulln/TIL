---
dg-publish: true
title: 主流的Kafka监控框架
createTime: 2023-07-22 23:56  
---
## 主流的Kafka监控框架

### JMXTool 工具

```shell
bin/kafka-run-class.sh kafka.tools.JmxTool
```

![](https://static001.geekbang.org/resource/image/79/d3/795399a24e665c1bf744085b5344f5d3.jpg?wh=1763*1103)

- 设置 --jmx-url 参数的值时，需要指定 JMX 端口。在这个例子中，端口是 9997，在实际操作中，你需要指定你的环境中的端口。

### Kafka Manager

Kafka Manager 提供了这样的功能。你可以修改 config 下的 application.conf 文件，删除 application.features 中的值。

### JMXTrans + InfluxDB + Grafana

现在更流行的做法是，在一套通用的监控框架中监控 Kafka，比如使用 JMXTrans + InfluxDB + Grafana 的组合。

### Confluent Control Center

Control Center 不但能够实时地监控 Kafka 集群，而且还能够帮助你操作和搭建基于 Kafka 的实时流处理应用。更棒的是，Control Center 提供了统一式的主题管理功能。你可以在这里享受到 Kafka 主题和 Schema 的一站式管理服务。

你需要付费才能使用。如果你需要一套很强大的监控框架，你可以登录 Confluent 公司官网，去订购这套真正意义上的企业级 Kafka 监控框架。



# 地址

此文章为7月day22 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/127192》
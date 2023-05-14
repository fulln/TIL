---
dg-publish: true
title: es介绍与安装
createTime: 2023-05-14 15:09  
---

### es的诞生

1. 分布式，可水平扩展
2. 高可用
3. 支持不同节点类型

#### 主要功能

1. 海量数据分户存储与集群管理
2. 近实时搜索，性能卓越
	1. 结构化/全文/地理位置/自动完成
3. 近实时分析
	1. 聚合

### 主要家族成员

1. KIBANA
2. logStash
3. beats
4. X-pack


### 安装与简单配置

#### 文件目录结构

| 目录    | 配置文件           | 描述                                    |     |
| ------- | ------------------ | --------------------------------------- | --- |
| bin     |                    | 脚本文件，包括启动es，安装插件等        |     |
| config  | elasticsearch.YAML | 集群配置文件，user, role_based 相关配置 |     |
| JDK     |                    | java运行环境                            |     |
| data    | path.data          | 数据文件                                |     |
| lib     |                    | Java类库                                |     |
| logs    | path.log           | 日志文件                                |     |
| modules |                    | 包含所有ES模块                          |     |
| plugins        |                    |包含所有已安装插件                                         |     |
#### JVM 配置

内存不要超过30GB

### 多个es实例运行

```shell
bin/elasticsearch -E node.name=node1 -E cluster.name=esnodes  -E path.data==node2_data -d
bin/elasticsearch -E node.name=node2 -E cluster.name=esnodes  -E path.data==node2_data -d
bin/elasticsearch -E node.name=node3 -E cluster.name=esnodes  -E path.data==node3_data -d
```

集群记得设置map_count
```shell
sudo sysctl -w vm.max_map_count=262144
```


### kibana 安装下载

### Logstash安装使用

#### logstash.yml
```YML
node.name: logstash-203
# 日志文件目录配置
path.logs: /usr/share/logstash/logs
# 验证配置文件及存在性
config.test_and_exit: false
# 配置文件改变时是否自动加载
config.reload.automatic: false
# 重新加载配置文件间隔
config.reload.interval: 60s
# debug模式 开启后会打印解析后的配置文件 包括密码等信息 慎用
# 需要同时配置日志等级为debug
config.debug: true
log.level: debug
# The bind address for the metrics REST endpoint.
http.host: 0.0.0.0
```

#### pipelines.yml

```YML
- pipeline.id: main 
- path.config: /usr/share/logstash/config/logstash.conf
```




# 地址

此文章为5月day14 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-102659》
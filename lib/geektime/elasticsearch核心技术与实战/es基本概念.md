---
dg-publish: true
title: es基本概念
createTime: 2023-05-17 20:56  
---

## 基础概念

1. Elasticsearch是面向文档的，是所有可搜索数据的最小单元
2. 文档会被序列化成JSON格式，保持在es中
	1. 文档包含一系列字段
	2. 文档元数据
		1. ____index 索引名
		2. ____type 类型名
		3. ____id 唯一id
		4. ____source 原始json
		5. ____version 版本信息
		6. ____score 相关性打分
	3. 索引 文档的结合
		1. index，体现了逻辑空间概念
		2. shard 体现物理空间概念
		3. mapping 定义文档字段类型
		4. setting 定义不同数据分布
		5. type
			1. 一个索引只能创建一个Type
3. 每个文档都有UniqueId
4. 传统关系型数据库和Es的区别
	1. es-schemaless /相关性/高性能全文索引
	2. RDMS /事务性/Join

#### 分布式系统的可用和扩展性

1. 高可用性
	1. 服务可用性
	2. 数据可用性
2. 可扩展性
3. es分布好处
	1. 水平扩容
##### 节点
1. 节点就是es的实例
	1. 本质是java进程
	2. 一台机器可以运行多个es进程，但是建议只运行一个
2. 节点都有名字
3. 启动后会分配uuid

#### Master-eligible 和 Master
- 每个节点启动后默认就是Master-eligible节点
- Master-eligible 可以参加主流程
- 第一个节点启动时，会将自己选举成master节点
- 每个节点上都保存了集群状态，只有master可以修改

#### DataNode 和 Coordinating Node

- DataNode： 可以保存数据的节点，保存分片数据，在数据扩展上起到关键作用
- Coordinating Node
	- 接受Client 请求，分发到合适节点，最后把结果汇集
	- 每个节点默认都起了Coordinating Node的职责

#### Other

- HOT & WarmNode
- MachineLearningNode
- TribeNode

### 配置节点类型

生产环境，应该设置单一的角色节点
| 节点类型          | 配置参数    | 默认值       |
| ----------------- | ----------- | ------------ |
| master eligible   | node.master | true         |
| data              | node.data   | true         |
| ingest            | node.ingest | true         |
| coordinating only | 无          | 每个节点都是 |
| machine learing                  | node.ml             | true              |

### 分片

- 主分片，用于解决数据水平扩展的问题
	- 一个分片是一个运行的Lucene 实例
	- 主分片数在创建时指定，不允许修改，除非reindex
- 副本，用于解决数据高可用的问题，分片时主分片的拷贝
	- 可以动态调整副本数
	- 增加副本数，可以一定程度上提高可用性
- 设定
	- 分片数设置过小
		- 后续无法增加节点实现水平扩展
		- 单个分片数据量太大导致数据分配耗时
	- 分片数过大。7.0 默认主分片设置为1，解决over-sharding的问题
		- 影响搜索结果的相关性打分
		- 单节点上过多分片，导致资源浪费，也影响性能

### 演示

- 查看集群的健康状态
http://localhost:9200/_cluster/health
- CAT api
	- http://localhost:9200/_cat/nodes_
- 设置分片数


# 地址 

此文章为5月day17 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-102666》
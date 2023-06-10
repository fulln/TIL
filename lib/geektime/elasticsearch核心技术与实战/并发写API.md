---
dg-publish: true
title: 并发读写操作
createTime: 2023-06-10 22:51  
---

## es的乐观并发控制

- es的文档是不可变的
	- 删除文档，同时新增一个文档并version+1
- 内部版本控制
	- if_seq_no + lf_primary_term
- 使用外部版本，使用其他数据库做主要数据存储
	- version+version_type = extrenal


```http

PUT products/_doc/1?version=30000&version_type=external
{
  "title":"iphone",
  "count":100
}

```

## 集群通信安全问题

- 为啥要加密通讯
	- 避免数据抓包
- 验证身份- 避免 Impostor Node
	- 通过TLS 加密节点数据
	- 节点创建证书
		- certificates 需要使用相同CA证书
		- Full Version 需要相同CA ,还需要验证hostName 和ip
		- 不采用任何验证 

### 生成CA 证书

- bin/elasticsearch-certutil ca 生成证书


# 地址

此文章为6月day10 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-114569》

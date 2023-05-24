---
dg-publish: true
title: Es聚合分析
createTime: 2023-05-24 21:52  
---

# 聚合

- es除了搜索之外，提供的针对es的数据分析的功能
	- 实时性高
	- hadoop
- 通过聚合，会得到一个数据的概览，是分析和总结全套的数据，而不是寻找单个文档
- 高性能，只需一条语句就可以从es得到结果
	- 无需在客户端实现分析逻辑

### 场景

kibana可视化报表

### 聚合的分类

- bucket Aggregation   一些满足特定条件的文档的集合
- Metric Aggregation 数学运算，可以对文档字段进行统计分析
- pipline Aggregation 对其他的聚合结果二次分析
- Matrix Aggregation 支持多个字段的操作并提供一个结果矩阵

### Bucket & Metric
- Bucket，桶 可以通过**Term & range**统计
- Metric 基于数据集计算结果，除了支持在字段上计算，也支持在脚本产生的结果上计算
	- 大多数Metric 是数学计算
	- 部分metric 支持输出多个值


```

#按照目的地进行分桶统计
GET kibana_sample_data_flights/_search
{
	"size": 0,
	"aggs":{
		"flight_dest":{
			"terms":{
				"field":"DestCountry"
			}
		}
	}
}

#查看航班目的地的统计信息，增加平均，最高最低价格
GET kibana_sample_data_flights/_search
{
	"size": 0,
	"aggs":{
		"flight_dest":{
			"terms":{
				"field":"DestCountry" 
			},
			"aggs":{
				"avg_price":{
					"avg":{
						"field":"AvgTicketPrice"
					}
				},
				"max_price":{
					"max":{
						"field":"AvgTicketPrice"
					}
				},
				"min_price":{
					"min":{
						"field":"AvgTicketPrice"
					}
				}
			}
		}
	}
}
#价格统计信息+天气信息
GET kibana_sample_data_flights/_search
{
	"size": 0,
	"aggs":{
		"flight_dest":{
			"terms":{
				"field":"DestCountry" // 根据地点第一次聚合
			},
			"aggs":{
				"stats_price":{
					"stats":{
						"field":"AvgTicketPrice"
					}
				},
				"wather":{
				  "terms": {
				    "field": "DestWeather",
				    "size": 5
				  }
				}

			}
		}
	}
}

```


### 产品和使用场景

- es提供如模糊查询，搜索条件，事务不如关系型数据库强大

#### 基本概念

- es集群可以运行在单节点，也可以运行在多个服务器上，实现数据和服务的水平扩展
- 索引是一些具有相似结构的文档的集合
- 物理角度看，分片是Lucene的实例，分片存储了索引的具体数据，可以分布在不同节点。副本分片除了提高数据可用性，还提升了集群的查询性能
- es的文档可以是任意json的数据
- 文档写入es的过程叫索引
- es提供了rest api

#### 搜索和aggregation

- Precosion 指除了返回相关结果还返回了不相干的
- Recall 衡量有多少相关的结果，实际上没有返回的
- 精确值包括数字，日期和某些具体的字符串
- 全文本，是需要被检索的非结构文本
- Analyis 将文本转成倒排索引的Terms的过程
- es的Analyzer是Char_filter ->Tokenizer -> TokenFilter 的过程
- 善于利用_analyze API 测试Analyzer
- es 支持 URL Search和requestBody 方式
- es提供这几种：[[#聚合的分类]]


#### 文档的CRUD 和 index Mapping

- 从性能上说，建议使用bulk，mget，msearch 等操作，但是单次操作的数据量不要过大，以免引发性能问题
- 每个索引有Mapping定义，包含文档字段及类型，字段的Analyzer的相关配置
- Mapping可以被动态的创建，为了避免一些错误的类型推算，可以显示定义Maping
- Mapping可以动态创建，也可以显示定义 
- 可以为指定字段定制化Analyzer，也可以为查询字符串指定 search_analyzer
- index Template 可以定义Mapping 和settings，并自动更新到新创建的索引上，
- Dynamic Template 支持在具体的索引上指定规则，为新增的字段指定对应mapping

# 地址

此文章为5月day24 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-106166》
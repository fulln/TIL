---
dg-publish: true
title: Analyzer
createTime: 2023-05-19 22:02  
---

# Analuzer 和 Analysis

- Analysis 把全文转换一系列单词的过程，也就是分词
- Analysis 通过Analuzer实现
	- 用es的内置分词器/按需定制化分析器
- 除了写入时转换词条，匹配Query 也需要相同的分析器对查询语句进行分析

### 组成

分词器由3个部分组成
- Character Filter 针对原始文本处理
- Tokenizer 按照规则切分为单词
- Token Filter 小写，删除stopwords，增加同义词

####  使用api
```es
GET /_analyze
{
  "analyzer": "standard",
  "text": "mastring elasticsearch ,elasticsearch in action"
}
```

- 直接指定Analyzer 测试
- 指定索引的字段测试
- 自定义分词进行测试

#### standard analyzer
- 默认分词器
- 按词切分
- 小写处理

#### 中文分词

- icu
- ik
- thulac

## Search Api 

- URI Search
	- url 使用查询参数
		- q来指定查询字符串
		- Query string syntax，kv键值对
- request boyd search
	- es提供的，基于json格式DSL
	- 返回值介绍
		- took 花费时c间
		- total 总文档数
		- hits 结果集，默认前10文档
			- _INDEX 索引名
			- _ID 文档id
			- _score 打分
			- _source 文档原始信息

### 搜索的相关性
- Precision 查准率 /全部返回的结果
- Recall 查全率/ 应该返回的结果
- Ranking 相关度排序





# 地址

此文章为5月day19 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-104929》
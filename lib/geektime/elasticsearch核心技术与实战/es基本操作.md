---
dg-publish: true
title: es基本操作
createTime: 2023-05-18 21:35  
---

# 文档的crud与批量操作

### 文档crud
- Type 名，约定都用_DOC
- Create  如果id已经存在，会失败
	- 支持自动生成id和指定id
	- 使用 http PUT 创建时，url中显示指定_CREATE
- GET 找到文档，返回200，找不到返回404 
	- 文档元信息
	- 版本信息，同一个ID的文档，即使删除，Version也会不断增加
	-  SOURCE 默认包含所有原始信息 
- index 如果id不存在，创建新文档，否则先删除现有文档
	- 和create不一样的地方：文档不存在则创建，否则现有文档被删除，新文档被索引，版本+1
- Update 文档必须已经存在，更新只对响应字段做增量修改
	- 不删除原来的文档
- Bulk API
	- 支持一次调用中，对不同索引进行操作
	- 支持四种
		- index
		- create
		- update
		- delete
	- 可以在url中指定index,也可以在Payload
	- 操作单条失败，不影响其他操作
	- 返回结果包括每一条结果
- Mget API 批量读取
	- /_MGET
- Msearch 批量查询
	- __MSEARCH

### 倒排索引

正排：文档id ->单词
倒排：单词 -> 文档id

#### 组成

1. 单词词典
	1. 记录所有文档的单词，单词到倒排的关联关系
		1. 通过b+树或者hash拉链法实现
2. 倒排列表，单词对应文档结合
	1. 倒排索引项
		1. 文档id
		2. 词频
		3. 位置
		4. 偏移（offset）

es的json文档每个字段，都有自己的倒排索引，不过可以指定某个字段不索引


# 地址

此文章为5月day18 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-102668》
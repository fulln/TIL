

### 高级查询

1. 支持多项文本输入,针对字段进行搜索
2. 搜索引擎一般也提供基于时间,价格等条件的过滤
3. es中,有Query 和Filter2种不同的context
	1. Query Context: 相关性算分
	2. Filter Context : 不需要算分

#### bool查询

- 一个bool 查询是一个或者多查询子句的组合
	- 总共4种子句,2种影响算分,2种不影响
- 相关性不只是全文本检索的专利,也适用 yes|no的子句,匹配的子句越多,相关性越高. 

| must     | 必须匹配,贡献算分               |
| -------- | ------------------------------- |
| shuold   | 选择性匹配,贡献算分             |
| must not | Filter Context 必须不匹配       |
| filter   | Filter Context  必须匹配,不算分 |

- 子查询可以任意出现
- 可以嵌套多个查询
- 如果你的bool查询,没有must条件,should 必须满足一条查询

### 如何查询包含不是相等的问题
- 增加genre count字段计数
- 使用bool查询

#### 嵌套查询
#### 查询语句的结构,对相关性产生影响
- 同一层下的竞争字段,具有相同的权重
- 通过嵌套bool查询,改变对算分的影响

控制字段的boosting,影响算分

#### NOT quite NOT

1. must not
2. boosting
	1. positive
	2. negative
	3. negative_boost: 0.5

# 地址

此文章为5月day27 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-108287》
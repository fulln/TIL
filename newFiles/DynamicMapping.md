---
dg-publish: true
title: DynamicMapping
createTime: 2023-05-21 21:43  
---

### Query String

- 使用`query_string` 关键字

```es
POST users/_search
{
  "query": {
    "query_string": {
      "default_field": "name",
      "query": "Ruan AND Yiming"
    }
  }
}
```

### Simple Query String Query

- 类似Query String ，但是会忽略错误的语法，只支持部分查询语法
- 不支持AND OR NOT，当字符串处理
- Term 默认的关系是 OR，指定 `default_operator`
- 支持部分逻辑
	- +
	- |
	- -

```
#Simple Query 默认的operator是 Or
POST users/_search
{
  "query": {
    "simple_query_string": {
      "query": "Ruan AND Yiming",
      "fields": ["name"]
    }
  }
}
```

### Mapping & Dynamic Mapping

- Mapping 类似数据库中的schema定义，作用如下
	- 定义索引中的字段名
	- 定义字段数据类型，如字符串，数字，布尔
		- 简单类型
			- Text/ keyword
			- Date
			- Integer/Floating
			- Boolean
			- IPV4 & IPV6
		- 复杂类型，对象和嵌套对象
		- 对象类型 / 嵌套类型
		- 特殊类型
			- geo_point & geo_shape / percolator
	- 字段，倒排索引的相关配置
- mapping 会把json文档映射成Lucene 需要的扁平字段
- 一个Mapping 属于一个所应的Type
	- 每个文档都属于一个Type
	- 一个Type有一个Mapping定义
	- 不需要再Mapping 定义中指定type信息

#### Dynamic Mapping

- 写入文档时，如果索引不存在，则自动创建索引
- Dynamic Mapping的机制，使得我们无需手动定义Mappings，es进行类型的自动识别
- 有时候会推算不对
- 当类型设置不对时，导致一些功能无法正常运行


##### 类型的自动设别

| json类型 | es类型                                                                                         |
| -------- | ---------------------------------------------------------------------------------------------- |
| 字符串   | - 匹配日期格式<br> -匹配数字设置为float or long 默认关闭 <br>- 设置为Text，并增加keyword子字段 |
| 布尔值   | boolean                                                                                        |
| 浮点数   | float                                                                                          |
| 整数     | long                                                                                           |
| 对象     | object                                                                                         |
| 数组     | 由第一个非空数值的类型决定                                                                     |
| 空值     | 忽略                                                                                               |

```

#dynamic mapping，推断字段的类型
PUT mapping_test/_doc/1
{
    "uid" : "123",
    "isVip" : false,
    "isAdmin": "true",
    "age":19,
    "heigh":180
}

#查看 Dynamic
GET mapping_test/_mapping

```

##### 能否更改Mapping字段类型

- 两种情况
	- 新增
		- Dynamic = ture，一旦由新增字段的文档写入，Mapping 也同时更新
		- Dynamic = false，Mapping 不会被更新，新增字段无法索引，但是信息会出现在source
		- Dynamic = Strict ，文档写入失败
	- 对已有字段，一旦由数据写入，就不支持修改定义
		- Lucene实现的倒排索引，一旦生成，不运行修改
	- 如果希望改变，必须reindex api，重建索引
- 原因
	- 如果修改了数据类型，导致已有数据无法被索引
	- 如果是新增的字段，则不会有该影响


# 地址

此文章为5月day21 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-105684》
---
dg-publish: true
title: uriSearch
createTime: 2023-05-20 19:06  
---

## 参数

- q 指定查询语句，使用Query String Syntax 
	- 指定查询 vs 泛查询
		- q=title:2012 / q=2012
	- Term vs Phrase
		- Beautiful Mind  = Beautiful OR Mind   
		- "Beautiful Mind " = Beautiful AND Mind ，Phrase 要求前后顺序一致  
	- Bool 操作
		- AND / OR / NOT 或者 && / || / !
		- 分组
			- + 表示must
			- - 表示must not
	- 范围查询
		- 区间表示：[]闭区间，{} 开区间
			- year:{2019 TO 2018}
			- year:[* TO 2018]
	- 算术符号
		-  year: > 2010
		-  year: (> 2010 && <= 2018)
		-  year:(+>2010 +<=2018)
	- 通配符查询（查询效率低，占用内存大，不建议使用，特别是放最前）
		- ？表1个字符，*  代表0or多个字符
		- 正则表达
			- title：[bt]oy
		- 模糊匹配与近似查询
			- title：beautiful ~ 1
			- title："lord ring" ~ 2
```ES
# QSS
GET /movies/_search?q=2012&df=title&sort=year:desc&from=0&size=10&timeout=1s

#  Phrase Query：
GET /movies/_search?q=title:"Beautiful Mind"
{
	"profile":"true"
}
# Term Query:
GET /movies/_search?q=title:(Beautiful Mind)
{
	"profile":"true"
}
# bool 操作 - must 查找美丽心灵
GET /movies/_search?q=title:(Beautiful %2BMind)
{
	"profile":"true"
}
#  bool 操作 - and 查找美丽心灵
GET /movies/_search?q=title:(Beautiful AND Mind)
{
	"profile":"true"
}
# 通配符查询
GET /movies/_search?q=title:b*
{
	"profile":"true"
}
# 模糊匹配&近似度匹配
GET /movies/_search?q=title:beautifl~1
{
	"profile":"true"
}
```

- df默认字段， 不指定时，对所有字段进行查询
	- 指定字段查询 -> 1
	- 不使用df的话，使用q传字段名:值来进行查询 -> 2
```ES
// 1.
GET /movies/_search?q=2012&df=title
{
	"profile":"true"
}
// 2.
GET /movies/_search?q=title:2012
{
	"profile":"true"
}
```
	 - 泛查询
```ES
GET /movies/_search?q=2012
{
	"profile":"true"
}
```
- Sort 排序/ from 和size 进行分页
- Profile 可以查看查询如何被执行的

## Request Body Search

- 将查询语句通过request body 发送到es
- Query DSL
- 分页：from，size
- 排序：sort
- source filtering
	- 如果source 没有存储，只返回匹配的文档元数据
	- 支持使用通配符
- 脚本字段:用脚本获取一个新的字段
	- script_fields
- 使用查询表达式-Match
	- Phrase
		- slop 近似值
	- Trem


```
# 1 基本查询
GET /movies,404_idx/_search?ignore_unavailable=true
{
	"profile":"true",
	"query":{
		"match_all":{}
	}
}

#2. 对日期排序
POST kibana_sample_data_ecommerce/_search
{
  "sort":[{"order_date":"desc"}],
  "query":{
    "match_all": {}
  }
}

#脚本字段
GET kibana_sample_data_ecommerce/_search
{
  "script_fields": {
    "new_field": {
      "script": {
        "lang": "painless",
        "source": "doc['order_date'].value+'hello'"
      }
    }
  },
  "query": {
    "match_all": {}
  }
}

# match or 查询
POST movies/_search
{
  "query": {
    "match": {
      "title": "last christmas"
    }
  }
}
# match and 查询
POST movies/_search
{
  "query": {
    "match": {
      "title": {
        "query": "last christmas",
        "operator": "and"
      }
    }
  }
}

# match 短语查询，近似查询 
POST movies/_search
{
  "query": {
    "match_phrase": {
      "title":{
        "query": "one love",
        "slop": 1
      }
    }
  }
}
```


# 地址

此文章为5月day20 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-104957》
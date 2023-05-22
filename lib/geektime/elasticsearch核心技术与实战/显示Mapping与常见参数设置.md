---
dg-publish: true
title: 显示Mapping与常见参数设置
createTime: 2023-05-22 21:28  
---

## 定义一个Mapping

- 参考API手册
- 为了减少输入的工作量，减少出错概率，可以按照下面步骤
	- 创建一个临时index，写入样本数据
	- 访问Mapping API 获取该临时文件的动态Mapping定义
	- 修改后用，使用该配置创建索引
	- 删除临时索引

```
DELETE users
PUT users
{
    "mappings" : {
      "properties" : {
        "firstName" : {
          "type" : "text"
        },
        "lastName" : {
          "type" : "text"
        },
        "mobile" : {
          "type" : "text",
          "index": false
        }
      }
    }
}
```

#### 控制当前字段是否被索引

- Index - 控制当前字段是否被索引，默认true，如果设置false，该字段不可被搜索
- Index options
	- 四种不同级别的Index Options配置，可以控制倒排索引记录的内容
		- docs - 记录doc id
		- freqs - 记录 doc id 和 term frequencies
		- Positions -记录 doc id / term frequencies/term position
		- offsets - doc id  / term frequencies/term position / character offects
	- Text 类型默认记录类型 positions ，其他默认为docs
	- 记录内容越多，占用存储空间越大

#### null value
- 需要对Null 实现搜索
- 只有keyword类型支持设定null value

```

DELETE users
PUT users
{
    "mappings" : {
      "properties" : {
        "firstName" : {
          "type" : "text"
        },
        "lastName" : {
          "type" : "text"
        },
        "mobile" : {
          "type" : "keyword",
          "null_value": "NULL"
        }

      }
    }
}
```

#### copy_to 设置
- _ all 在7中被 copy_to 替代
- 满足一些特定的搜索需求
- copy to 将字段的数值拷贝到目标字段，实现all的作用
- copy to 的目标字段不出现在_ source 中

```
#设置 Copy to
DELETE users
PUT users
{
  "mappings": {
    "properties": {
      "firstName":{
        "type": "text",
        "copy_to": "fullName"
      },
      "lastName":{
        "type": "text",
        "copy_to": "fullName"
      }
    }
  }
}
```
#### 数组类型

- es中不提供专门的数组类型，但是任何字段，都可以包含多个相同类类型的数值

```

PUT users/_doc/1
{
  "name":"twobirds",
  "interests":["reading","music"]
}

POST users/_search
{
  "query": {
		"match_all": {}
	}
}
```

## 多字段特性及Mapping中配置自定义Analyzer

- 特性
	- 精确匹配
		- 增加一个keyword
	- 使用不同的Analyzer
		- 不同语言
		- 拼音字段搜索
		- 为搜索和索引指定不同的analyzer

#### Excat values & Full Text

- Exact Value： 包括数字/ 日期 /具体一个字符串
	- Es中的keyword
	- 不需要被分词
		- 为每一个字段创建倒排索引
- 全文本，非结构化的文本数据
	- es中的text

#### 自定义分词
- character Filters
	- 在Tokenizer 之前对文本进行处理，增加删除及替换字符，可以配置多个Character Filters，会影响Tokenizer的position 和offset 信息
	- 自带的Character Filters
		- html strip  - 去除html标签
		- Mapping - 字符串替换
		- Pattern replace - 正则匹配替换

```

#使用char filter进行替换
POST _analyze
{
  "tokenizer": "standard",
  "char_filter": [
      {
        "type" : "mapping",
        "mappings" : [ "- => _"]
      }
    ],
  "text": "123-456, I-test! test-990 650-555-1234"
```


#### Tokenizer
- 将原始的文本按照一定规则，切分为词（term or token）
- es内置Tokenizers
	- whitespace / standard / uax_url email / pattern / keyword / path hierarchy
- 可以用java开发插件，实现自己的tokenizer
```

POST _analyze
{
  "tokenizer":"keyword",
  "char_filter":["html_strip"],
  "text": "<b>hello world</b>"
}


POST _analyze
{
  "tokenizer":"path_hierarchy",
  "text":"/user/ymruan/a/b/c/d/e"
}

```


#### Token Filters
- 将Tokenizer输出的单词，进行增加，修改， 删除
- 自带Token Filters
	- 小写 / stop / 近义词

```
# remove 加入lowercase后，The被当成 stopword删除
GET _analyze
{
  "tokenizer": "whitespace",
  "filter": ["lowercase","stop","snowball"],
  "text": ["The gilrs in China are playing this game!"]
}
```

#### Index Template


# 地址

此文章为5月day22 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-105687》

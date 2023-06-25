---
dg-publish: true
title: Ingest Pipline & Painless Script
createTime: 2023-06-19 23:11  
---

## 修复与增强写入的数据

- Tags字段中，逗号分隔的文本应该是数组，而不是字符串
- 后期需要对tags 进行aggs统计

## Ingest Node

- 默认下，每一个节点都是Ingest Node
	- 具有预处理的能力，可拦截Index和Bulk APi能力
	- 对数据进行转换，并重新返回给 Index 或Bulk Api
- 无需LogStash，就可以进行数据的预处理
	- 为某字段设置默认值，重命名字段名，对字段值进行split操作
	- 支持设置Painless 脚本，对数据进行更加复杂的加工

## Pipline & Processor
- pipline - 对通过的数据，按照顺序进行加工
- Porcessor - es对一些加工的行为进行抽象包装
	- es有很多内置的processor,也支持插件形式实现自己的Processor

```http
  

# 测试split tags

POST _ingest/pipeline/_simulate

{

  "pipeline": {

    "description": "to split blog tags",

    "processors": [

      {

        "split": {

          "field": "tags",

          "separator": ","

        }

      }

    ]

  },

  "docs": [

    {

      "_index": "index",

      "_id": "id",

      "_source": {

        "title": "Introducing big data......",

        "tags": "hadoop,elasticsearch,spark",

        "content": "You konw, for big data"

      }

    },

    {

      "_index": "index",

      "_id": "idxx",

      "_source": {

        "title": "Introducing cloud computering",

        "tags": "openstack,k8s",

        "content": "You konw, for cloud"

      }

    }

  ]

}
```


# 地址

此文章为6月day19 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-120987》
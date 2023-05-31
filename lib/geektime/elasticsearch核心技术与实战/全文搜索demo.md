---
dg-publish: true
title: 全文搜索demo
createTime: 2023-05-31 22:35  
---

## 查询demo

### 写入数据

### 查询并高亮

## Search Template和Index Alias 查询

### search Template
- 对相关性算分/ 查询性能都至关重要
- 在开发初期，可以明确查询参数，但是往往不能最终定义DSL的具体结构
	- 不过可以通过Search Template 定义Contract


```
POST _scripts/tmdb
{
  "script": {
    "lang": "mustache",
    "source": {
      "_source": [
        "title","overview"
      ],
      "size": 20,
      "query": {
        "multi_match": {
          "query": "{{q}}",
          "fields": ["title","overview"]
        }
      }
    }
  }
}


GET _scripts/tmdb

POST tmdb/_search/template
{
    "id":"tmdb",
    "params": {
        "q": "basketball with cartoon aliens"
    }
}
```

### index Alias 零停机运维

索引别名： 指定别名，在其他地方通过alais实现读写

```
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "movies-2019",
        "alias": "movies-latest"
      }
    }
  ]
}

POST movies-latest/_search
{
  "query": {
    "match_all": {}
  }
}
```




# 地址

此文章为5月day31 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-109502》
---
dg-publish: true
title: Term & Phrase Suggester
createTime: 2023-06-02 22:28  
---

## 什么是搜索建议

- 现代的搜索引擎，一般提供Suggest as you type
- 帮助用户在搜索的过程中，进行自动补全或者纠错
- google搜索后，一开始自动补全，一定长度后，开始提示相似的词

## Es suggest API

- 将输入的文本分解为token，在索引字典查找相似的term返回
- 根据不同的使用场景，es设计了4种类别的suggest
	- term & Phrase Suggest
	- Complete & Context Suggester

### Term Suggester

- suggest 就是一种特殊类型的搜索。text就是调用提供的文本，通常来自用户界面上输入的内容

```http
POST /articles/_search
{
  "size": 1,
  "query": {
    "match": {
      "body": "lucen rock"
    }
  },
  "suggest": {
    "term-suggestion": {
      "text": "lucen rock",
      "term": {
        "suggest_mode": "missing",
        "field": "body"
      }
    }
  }
}

# 可以搜索到rock
POST /articles/_search
{
  "suggest": {
    "term-suggestion": {
      "text": "lucen rock",
      "term": {
      // 加上 prefix_length: 0 开始模糊搜索后面的匹配内容
        "suggest_mode": "popular",
        "field": "body"
      }
    }
  }
}
```

phrase 控制搜索范围，一般比term的参数多

```

POST /articles/_search
{
  "suggest": {
    "my-suggestion": {
      "text": "lucne and elasticsear rock hello world ",
      "phrase": {
        "field": "body",
        "max_errors":2,
        "confidence":0,
        "direct_generator":[{
          "field":"body",
          "suggest_mode":"always"
        }],
        "highlight": {
          "pre_tag": "<em>",
          "post_tag": "</em>"
        }
      }
    }
  }
}
```

## Completion Suggester

- 提供了自动完成的功能，每输入一个字符就发送一次查询
- 对性能要求高，es采用了不同的数据结构，并非倒排索引完成，而是采用Analyze的数据编码成FST和索引一起存放，FST被es加载进整个内存
- FST只能前缀查询


```
POST articles/_search?pretty
{
  "size": 0,
  "suggest": {
    "article-suggester": {
      "prefix": "elk ",
      "completion": {
        "field": "title_completion"
      }
    }
  }
}
```

- completion suggester扩展简单，在搜索上加入更多上下文

### 实现Context Suggester

- 定义2种类型的Context
	- Category - 任意字符串
	- Geo - 地理位置信息
- 实现Context Suggester的具体步骤
	- 定制Mapping
	- 索引数据，并且为每个文档加入Context信息
	- 结合Context 进行Suggestion查询

```http
POST comments/_search
{
  "suggest": {
    "MY_SUGGESTION": {
      "prefix": "sta",
      "completion":{
        "field":"comment_autocomplete",
        "contexts":{
          "comment_category":"coffee"
        }
      }
    }
  }
}
```

### 精准度和召回率

- 精准度
	- Completion > Phrase > Term
- 召回率
	- Term > Phrase > Completion
- 性能
	- Completion > Phrase > Term

# 地址

此文章为6月day2 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-111012》

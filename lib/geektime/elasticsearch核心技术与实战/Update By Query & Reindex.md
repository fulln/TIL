---
dg-publish: true
title: Update By Query & Reindex
createTime: 2023-06-18 23:35  
---

## 使用场景

- 一般需要重建索引
	- mapping 发生变更，字符类型更改，分词器及字典更新
	- 索引setting 变更，索引主分片发生改变
	- 集群内，集群数据迁移
- es内置api
	- update by query 现有索引上重建
	- reindex 其他所有上重建索引


### 索引增加子字段

```http
  

# 修改 Mapping，增加子字段，使用英文分词器

PUT blogs/_mapping

{

      "properties" : {

        "content" : {

          "type" : "text",

          "fields" : {

            "english" : {

              "type" : "text",

              "analyzer":"english"

            }

          }

        }

      }

    }
```

```http
  

# Update所有文档

POST blogs/_update_by_query

{

  

}
```

### 索引更改已有字段类型的Mappings

- es 不允许在原mapping修改
- 只能新建，并设定正确的类型，再切换

```http
  

# 创建新的索引并且设定新的Mapping

PUT blogs_fix/

{

  "mappings": {

        "properties" : {

        "content" : {

          "type" : "text",

          "fields" : {

            "english" : {

              "type" : "text",

              "analyzer" : "english"

            }

          }

        },

        "keyword" : {

          "type" : "keyword"

        }

      }    

  }

}
```

## Reindex API

- 支持把一个索引拷贝到另一个索引
- 使用Reindex Api的一些场景
	- 修改索引的主分片数
	- 改变字段的Mapping中的字段类型
	- 集群内数据迁移/跨集群的数据迁移

### 注意

- 要求enable source字段
- 当希望index设定时，先设置mapping，再执行reindex api
- reindex 只创建不存在的文档
- 文档存在，会导致版本冲突
- 跨集群reindex 设置 reindexx.REMOTE.Whitelist,并重启节点



# 地址

此文章为6月day18 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-120986》
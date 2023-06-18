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


# 地址

此文章为6月day18 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-120986》
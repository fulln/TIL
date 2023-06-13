---
dg-publish: true
title: Bucket & Metric 聚合分析
createTime: 2023-06-13 21:50  
---

## 聚合分析

- Metric 统计
- Bucket 一组满足条件的文档


### Aggregation的语法

Aggregation 属于search的一部分，一般建议将size指定为0
- 缩写 aggs
- 自定义聚合名字

```http
POST employees/_search
{
  "size": 0,
  "aggs": {
    "min_salary": {
      "min": {
        "field":"salary"
      }
    },
    "max_salary": {
      "max": {
        "field":"salary"
      }
    }
  }
}

```

一次聚合返回多个值

```http
POST employees/_search
{
  "size": 0,
  "aggs": {
    "stats_salary": {
      "stats": {
        "field":"salary"
      }
    }
  }
}

```

### Bucket Application

- Terms Aggs 
	- 字段需要打开filedData，才能执行
	- keyword 默认支持doc_value
	- Text 需要在Mapping中enable，会按照分词后的结果进行查询

```http
  

# 对keword 进行聚合

POST employees/_search

{

  "size": 0,

  "aggs": {

    "jobs": {

      "terms": {

        "field":"job.keyword"

      }

    }

  }

}
```

 对job.keyword 和 job 进行 terms 聚合，分桶的总数并不一样,统计总数
```http
POST employees/_search

{

  "size": 0,

  "aggs": {

    "cardinate": {

      "cardinality": {

        "field": "job"

      }

    }

  }

}
```

指定 bucket 的 size

```http
POST employees/_search

{

  "size": 0,

  "aggs": {

    "ages_5": {

      "terms": {

        "field":"age",

        "size":3

      }

    }

  }

}
```


指定size，不同工种中，年纪最大的3个员工的具体信息

```http
POST employees/_search

{

  "size": 0,

  "aggs": {

    "jobs": {

      "terms": {

        "field":"job.keyword"

      },

      "aggs":{

        "old_employee":{

          "top_hits":{

            "size":3,

            "sort":[

              {

                "age":{

                  "order":"desc"

                }

              }

            ]

          }

        }

      }

    }

  }

}
```

#### 优化Term聚合性能

- eager_global_ordinals : true
	- 写入的时候打开这个参数，可以优化Term的性能
	- 当聚合查询频繁，性能要求高，索引文档不断写入

###  数字类型
	- Range /Data Range
```http
POST employees/_search

{

  "size": 0,

  "aggs": {

    "salary_range": {

      "range": {

        "field":"salary",

        "ranges":[

          {

            "to":10000

          },

          {

            "from":10000,

            "to":20000

          },

          {

            "key":">20000",

            "from":20000

          }

        ]

      }

    }

  }

}
```
	- Histogram 聚合

 Salary Histogram,工资0到10万，以 5000一个区间进行分桶
```http
  


POST employees/_search

{

  "size": 0,

  "aggs": {

    "salary_histrogram": {

      "histogram": {

        "field":"salary",

        "interval":5000,

        "extended_bounds":{

          "min":0,

          "max":100000

  

        }

      }

    }

  }

}
```

### Bucket + metric Aggregation

- Bucket 聚合分析允许通过添加子聚合分析来进一步分析
	- Bucket
	- Metric

 多次嵌套。根据工作类型分桶，然后按照性别分桶，计算工资的统计信息
```http
POST employees/_search

{

  "size": 0,

  "aggs": {

    "Job_gender_stats": {

      "terms": {

        "field": "job.keyword"

      },

      "aggs": {

        "gender_stats": {

          "terms": {

            "field": "gender"

          },

          "aggs": {

            "salary_stats": {

              "stats": {

                "field": "salary"

              }

            }

          }

        }

      }

    }

  }

}
```

# 地址

此文章为6月day13 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-118147》

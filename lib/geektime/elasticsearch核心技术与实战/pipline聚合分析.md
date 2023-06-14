---
dg-publish: true
title: pipline聚合分析
createTime: 2023-06-14 22:44  
---


## 对聚合分析再聚合分析

- min_bucket
	-  结果和其他的聚合同级
	- min_bucket求之前结果的最小值
	- 通过bucket_path 关键字指定路径

### pipline
- 管道
	- 支持对聚合分析的结果，再次进行聚合分析
	- pipline的分析结果会输出到原结果中，根据位置的不同，分为：
		- sibling - 结果和现有分析结果同级
			- max，min，avg， sum bucket
			- stats, Extended status bucket
			- percentiles Bucket
		- parent 结果内嵌到现有的聚合分析结果
			- derivative （求导）
			- Cumultive sum（累计求和）
			- Moving Function （滑动窗口）



```HTTP  
# 平均工资最低的工作类型


POST employees/_search

{

  "size": 0,

  "aggs": {

    "jobs": {

      "terms": {

        "field": "job.keyword",

        "size": 10

      },

      "aggs": {

        "avg_salary": {

          "avg": {

            "field": "salary"

          }

        }

      }

    },

    "min_salary_by_job":{

      "min_bucket": {

        "buckets_path": "jobs>avg_salary"

      }

    }

  }

}
```

-  parent pipline

```http
#按照年龄对平均工资求导

POST employees/_search

{

  "size": 0,

  "aggs": {

    "age": {

      "histogram": {

        "field": "age",

        "min_doc_count": 1,

        "interval": 1

      },

      "aggs": {

        "avg_salary": {

          "avg": {

            "field": "salary"

          }

        },

        "derivative_avg_salary":{

          "derivative": {

            "buckets_path": "avg_salary"

          }

        }

      }

    }

  }

}
```

## 聚合的作用范围

- es聚合的默认作用范围是query的查询结果集
- 同时es支持改变作用范围
	- Filter
	- Post Filter
	- Global
QUERY:
```HTTP
POST employees/_search

{

  "size": 0,

  "query": {

    "range": {

      "age": {

        "gte": 20

      }

    }

  },

  "aggs": {

    "jobs": {

      "terms": {

        "field":"job.keyword"

      }

    }

  }

}
```
FILTER
```http
POST employees/_search

{

  "size": 0,

  "aggs": {

    "older_person": {

      "filter":{

        "range":{

          "age":{

            "from":35

          }

        }

      },

      "aggs":{

         "jobs":{

           "terms": {

        "field":"job.keyword"

      }

      }

    }},

    "all_jobs": {

      "terms": {

        "field":"job.keyword"

      }

    }

  }

}
```

Post field. 一条语句，找出所有的job类型。还能找到聚合后符合条件的结果

```http
POST employees/_search

{

  "aggs": {

    "jobs": {

      "terms": {

        "field": "job.keyword"

      }

    }

  },

  "post_filter": {

    "match": {

      "job.keyword": "Dev Manager"

    }

  }

}
```
global: 忽略query中的条件

```http
POST employees/_search

{

  "size": 0,

  "query": {

    "range": {

      "age": {

        "gte": 40

      }

    }

  },

  "aggs": {

    "jobs": {

      "terms": {

        "field":"job.keyword"

      }

    },

    "all":{

      "global":{},

      "aggs":{

        "salary_avg":{

          "avg":{

            "field":"salary"

          }

        }

      }

    }

  }

}
```

# 地址

此文章为6月day14 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-118148》
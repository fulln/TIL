---
dg-publish: true
title: indexTemplate
createTime: 2023-05-23 22:41  
---
## index Template

- index Templates  帮助你设定Mappings 和Settings ，并安卓一定的规则，自动匹配到新创建的索引上
	- 模板仅仅在一个索引被新创建的时候，才产生作用，修改模板不会影响已创建的索引
	- 可以设定多个索引模板，这些设置会被"merge"在一起
	- 可以指定"order"的数值，控制"merging"的过程

- 工作方式
	- 应用es默认的settings 和mappings
	- 应用order 数值低的Index Template 中的设定
	- 应用order 高的 Index Template的设定，之前的设定被覆盖
	- 应用创建索引时，用户指定的settings 和Mappings，覆盖模板中的设定


```shell
PUT /_template/template_test
{
    "index_patterns" : ["test*"],
    "order" : 1,
    "settings" : {
    	"number_of_shards": 1,
        "number_of_replicas" : 2
    },
    "mappings" : {
    	"date_detection": false, // 字符串转date 
    	"numeric_detection": true //字符串转数字
    }
}

#查看template信息
GET /_template/template_default
GET /_template/temp*
```

## Dynamic Template

- 根据es识别的数据类型，结合字段名，动态设定字段类型
	- 所有的字符串都设定成Keyword，或者关闭keyword字段
	- is开头的字段设置成boolean
	- long_ 开头的都设置为long类型

- Dynamic Tempate 是定义在索引的Mapping中
- Template 有名称
- 匹配规则是数组
- 为匹配到字段设置Mapping


```


GET my_index/_mapping
DELETE my_index
PUT my_index
{
  "mappings": {
    "dynamic_templates": [
            {
        "strings_as_boolean": {
          "match_mapping_type":   "string",
          "match":"is*",
          "mapping": {
            "type": "boolean"
          }
        }
      },
      {
        "strings_as_keywords": {
          "match_mapping_type":   "string",
          "mapping": {
            "type": "keyword"
          }
        }
      }
    ]
  }
}

PUT my_index
{
  "mappings": {
    "dynamic_templates": [
            {
        "strings_as_boolean": {
          "match_mapping_type":   "string",
          "match":"is*",
          "mapping": {
            "type": "boolean"
          }
        }
      },
      {
        "strings_as_keywords": {
          "match_mapping_type":   "string",
          "mapping": {
            "type": "keyword"
          }
        }
      }
    ]
  }
}
```

# 地址

此文章为5月day23 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100030501-106158》

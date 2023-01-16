#alg #redis

## 视频地址

https://www.bilibili.com/video/BV1J24y117CF


## 语法

-  \*  ： 任意数量字符
-  ？： 任意单字符
- [...]： 集合中的字符
- 其他字符： 严格匹配
- 转义符

### redis中的实现的问题


1.  \* 的使用是采用的dfs算法
	1.  \*很多，匹配的长度很长的情况下，栈会爆掉
	2.  匹配失败的情况下，会耗时很长，

### 其他的实现

- Python -> fnmatch ： 转RE,性能慢
- GO -> fnmatch： 回溯

### 算法特征

[05:06](https://www.bilibili.com/video/BV1J24y117CF#t=306.362147)

1.  只有 \* 匹配任意字符



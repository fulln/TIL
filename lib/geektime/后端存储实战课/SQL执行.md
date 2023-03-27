#lib #geektime #后端存储实战课 

# 10 | 走进黑盒：SQL是如何在数据库中执行的？

### 服务器执行

1. 执行器
2. 存储引擎

#### 如何执行

```sql
SELECT u.id AS user_id, u.name AS user_name, o.id AS order_id
FROM users u INNER JOIN orders o ON u.id = o.user_id
WHERE u.id > 50
```

把这一串文本解析成便于程序处理的结构化数据，这就是一个通用的语法解析过程。

转换后的结构化数据，就是一棵树，这个树的名字叫抽象语法树（AST，Abstract Syntax Tree）。

#### 主要优化点

1. 尽早地执行投影，去除不需要的列；
2. 尽早地执行数据过滤，去除不需要的行。

### sql如何在存储引擎执行

MySQL它在设计层面对存储引擎做了抽象，它的存储引擎是可以替换的。

1. 我们知道了 InnoDB 的索引实现后，就很容易明白为什么主键不能太长，因为表的每个索引保存的都是主键的值，过长的主键会导致每一个索引都很大
2. 有的时候明明有索引却不能命中的原因是，数据库在对物理执行计划优化的时候，评估发现不走索引，直接全表扫描是更优的选择

# 11 | MySQL如何应对高并发（一）：使用缓存保护MySQL




# 地址

此文章为3月day27 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/213176》，





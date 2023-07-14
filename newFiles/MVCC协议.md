---
dg-publish: true
title: MVCC协议
createTime: 2023-07-14 23:37  
---


## MVCC 协议

MVCC（Multi-Version Concurrency Control）中文叫做多版本并发控制协议，是 MySQL InnoDB 引擎用于控制数据并发访问的协议。它在面试中属于必面题，而且从 MVCC 出发能够将话题引申到事务、隔离级别两个重头戏上，所以掌握 MVCC 能让你进可攻退可守。

### 为什么需要mvcc
数据库和一般的应用有一个很大的区别，就是数据库即便是读，也不能被写阻塞住。

### 隔离级别

1. 读未提交（Read Uncommitted）是指一个事务可以看到另外一个事务尚未提交的修改。
2. 读已提交（Read Committed，简写 RC）是指一个事务只能看到已经提交的事务的修改。这意味着如果在事务执行过程中有别的事务提交了，那么事务还是能够看到别的事务最新提交的修改。
3. 可重复读（Repeatable Read，简写 RR）是指在这一个事务内部读同一个数据多次，读到的结果都是同一个。这意味着即便在事务执行过程中有别的事务提交，这个事务依旧看不到别的事务提交的修改。这是 MySQL 默认的隔离级别。
4. 串行化（Serializable）是指事务对数据的读写都是串行化的。

![](https://static001.geekbang.org/resource/image/3c/4b/3cec4b180e2a0a92bc6aa1c0d2de2c4b.png?wh=1920x750)

快照读和当前读。简单来说，快照读就是在事务开始的时候创建了一个数据的快照，在整个事务过程中都读这个快照；而当前读，则是每次都去读最新数据。MySQL 在可重复读这个隔离级别下，查询的执行效果和快照读非常接近


### 版本链

为了实现 MVCC，InnoDB 引擎给每一行都加了两个额外的字段 trx_id 和 roll_ptr。

1. trx_id：事务 ID，也叫做事务版本号。MVCC 里面的 V 指的就是这个数字。每一个事务在开始的时候就会获得一个 ID，然后这个事务内操作的行的事务 ID，都会被修改为这个事务的 ID。
2. roll_ptr：回滚指针。InnoDB 通过 roll_ptr 把每一行的历史版本串联在一起。

版本链。这个版本链存储在所谓的 undolog 里面，undolog 我们下一节课会详细讨论。

### Read View

前面你已经知道了 undolog 里面存放着历史版本的数据，当事务内部要读取数据的时候，Read View 就被用来控制这个事务应该读取哪个版本的数据。

Read View 最关键的字段叫做 m_ids，它代表的是当前已经开始，但是还没有结束的事务的 ID，也叫做活跃事务 ID。

**Read View 只用于已提交读和可重复读两个隔离级别**，

它用于这两个隔离级别的不同点就在于什么时候生成 Read View。
1. 已提交读：事务每次发起查询的时候，都会重新创建一个新的 Read View。
2. 可重复读：事务开始的时候，创建出 Read View。

#### Read View 与已提交读

在已提交读的隔离级别下，每一次查询语句都会重新生成一个 Read View。这意味着在事务执行过程中，Read View 是在不断变动的

#### Read View 与可重复读

在可重复读的隔离级别下，数据库会在事务开始的时候生成一个 Read View。这意味着整个 Read View 在事务执行过程中都是稳定不变的。我们用前面的例子来说明，就是在事务 A 开始的时候就会创建出来一个 Read View m_ids=2,3。


![](https://static001.geekbang.org/resource/image/cd/19/cd9e5fc6dccb166f3894ce0a7fb27f19.png?wh=1920x659)


# 地址

此文章为7月day14 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/675235》
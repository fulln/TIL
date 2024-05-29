---
createTime: 2024-05-08 17:09
tags:
---
## 基本概念
- 原子
- 一致
- 隔离
	- 隔离级别
		- 读未提交 read uncommitted
		- 读已提交 read committed
		- 可重复读（repeatable read）
		- 串行化（serializable ）
	- 实现
		- mvvc
		- undo log
			- 系统里没有比这个回滚日志更早的 read-view 的时候
			- 不要使用长事务
				 - 涉及到记录很难被自动清理
				 - 占用锁资源
- 持久

## 事务构成

### 事务id

1. 在事务开始的时候向 InnoDB 的事务系统申请,申请顺序严格递增
2. 先开始的事务获取的事务ID总是小于后开启的事务ID。 只读事务的ID和非只读事务的ID是有些区别的。前者是一个很大的数，后者是一个从1自增的数值。


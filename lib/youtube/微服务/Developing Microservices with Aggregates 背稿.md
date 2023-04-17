# 用聚合进行微服务开发


> 演讲提示:

欢迎来到关于微服务和领域驱动设计的演讲，这次是讲聚合，目的是真正展示聚合的概念是如何在你使用 微服务架构 构建业务逻辑 或业务应用程序时 的，事实证明，领域驱动设计对微服务的适用性比我谈论到的  要广泛得多

DDD的设计概念很多，比如有边界的背景和各种战略的概念 。但在这次演讲中，我只是专注于聚合的概念

---

# Presentation goal 

Show how Domain Driven Design Aggregates and Microservices are a perfect match
展示领域驱动设计聚合开发和微服务是怎么完美融合

> 演讲提示:



---
目录

- The problem with Domain Models and microservices / 领域模型和微服务的问题
- Overview of aggregates / 聚合概述
- Maintaining consistency between aggregates / 保持聚合之间的一致性
- Using event sourcing with Aggregates / 用聚合根进行事件溯源
- Customers and Orders example / 客户和订单的例子
- Using explicit saga orchestration / 使用显式的 saga 编排

> 演讲提示:

接下来我会讲述下正在使用领域模型和微服务中遇到的问题
然后我会讲怎么运用聚合处理他们之间的问题


---

The Microservice architecture tackles complexity through modularization
微服务架构通过模块化来解决复杂性。



---
Microservice = Business capability
微服务= 业务能力

---

Microservice architecture
微服务架构


---

But there are challenges…
但是仍然有些挑战

---

Domain model = tangled web of classes
领域模型 = 错综复杂的class 集合

---
Reliance on ACID transactions to enforce invariants
~~依赖 ACID 事务来强制执行不变量。~~
依赖 ACID 事务来保证最终一致性。

---
But it violates encapsulation…
但是他违反了封装性

---
.. and requires 2PC
还要去用2PC去保证一致性

---
2PC is not an option
2阶段提交不是一个可选择的选项

- Guarantees consistency 保持一致性

BUT

- 2PC coordinator is a single point of failure  单点故障
- Chatty: at least O(4n) messages, with retries O(n^2) 
- Reduced throughput due to locks  因锁而减少的吞吐量 
- Not supported by many NoSQL databases (or message brokers) 许多NoSQL数据库（或消息broker）不支持。
-  CAP theorem => 2PC impacts availability cap理论，2pc是影响的可用性
- ...

---
Doesn’t fit with the NoSQL DB “transaction” model
不符合NoSQL数据库的 "事务"模式

---
目录

- The problem with Domain Models and microservices / 领域模型和微服务的问题
- Overview of aggregates / 聚合概述
- Maintaining consistency between aggregates / 保持聚合之间的一致性
- Using event sourcing with Aggregates / 用聚合根进行事件溯源
- Customers and Orders example / 客户和订单的例子
- Using explicit saga orchestration / 使用显式的 saga 编排

> 演讲提示:


---

Domain Driven Design - building blocks

已经使用了的
- Entity 
- Value object 
- Services 
- Repositories 

忽略掉的
- Aggregates
---
About Aggregates

- Cluster of objects that can be treated as a unit
	对象集可以当作一个最小单元
- Graph consisting of a root entity and one or more other entities and value objects
	由一个根实体和一个或多个其他实体及值对象组成的Graph~~图谱~~
- Typically business entities are Aggregates, e.g. customer,Account, Order,Product, ….
典型的业务实体是聚合根，例如客户、账户、订单、 产品，....

---
Aggregate: rule #1

Reference other aggregate roots via identity (primary key) 

根据主键去引用其他聚合根

---
Foreign keys in a Domain Model?!?

在领域模型里面的外键？

---

Domain model = collection of loosely connected aggregates
领域模型 = 一组松散连接的聚合根

---
Easily partition into microservices

轻松地划分到微服务


---
Aggregate rule #2

Transaction = processing one command by one aggregate

事务=由一个聚合根处理一个命令

---
Transaction scope = service

事务范围 =  服务

---

Transaction scope = NoSQL database “transaction”

事务范围 =  NoSql 数据库的事务

---

目录

- The problem with Domain Models and microservices / 领域模型和微服务的问题
- Overview of aggregates / 聚合概述
- Maintaining consistency between aggregates / 保持聚合之间的一致性
- Using event sourcing with Aggregates / 用聚合根进行事件溯源
- Customers and Orders example / 客户和订单的例子
- Using explicit saga orchestration / 使用显式的 saga 编排

> 演讲提示:

---

How to maintain data consistency between aggregates?

如何保持聚合体之间的数据一致性？

---
Using event-driven Sagas instead of 2PC


https://zhuanlan.zhihu.com/p/95852045

---
Saga-based, eventually consistent order processing

基于Saga的 订单最终一致性处理

---
Eventually consistent credit checking

最终一致性 信用卡检查

---
Complexity of compensating transactions

补偿交易的复杂性

ACID transactions can simply rollback

事务可以简单回滚

BUT

Developer must write application logic to “rollback” eventually consistent transactions

开发者必须写应用逻辑去回滚一致性事务。


---

How atomically update database and publish an event

如何原子性更新数据库并发布事件

---


# 用聚合进行微服务开发


> 演讲提示:

欢迎来到关于微服务和领域驱动设计的演讲，这次是讲聚合，目的是真正展示聚合的概念是如何在你使用微服务架构构建业务逻辑或业务应用程序时的用处，事实证明，领域驱动设计对微服务的适用性比我所谈论的要广泛得多

DDD的设计概念很多，但在这次演讲中，我只是专注于聚合的概念

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

接下来我会讲述下正在使用领域模型和微服务中遇到的问题
然后我会讲怎么运用聚合处理他们之间的问题

---

The Microservice architecture tackles complexity through modularization
微服务架构通过模块化来解决复杂性。



---
Microservice = Business capability
微服务= 业务能力

---

---
dg-publish: true
---

#java #dubbo #极客时间 

## 课程内容

### dubbo缓存

先查询缓存，有数据则直接使用，没有数据再发起远程调用，拿到远程调用的结果后再放到缓存中

#### Dubbo Cache Filter

- CacheFilter 是 Dubbo 的一个核心组件。
- 启用缓存键属性，将会缓存 method 的返回值。
- 需要为缓存键属性配置缓存类型，类型有 lru、threadlocal、jcache、expiring 四种。

##### 使用方式

```xml
	 1)<dubbo:service cache="lru" />
     2)<dubbo:service /> <dubbo:method name="method2" cache="threadlocal" /> <dubbo:service/>
     3)<dubbo:provider cache="expiring" />
     4)<dubbo:consumer cache="jcache" />
```

##### 可选择策略

- threadlocal，使用的是 ThreadLocalCacheFactory 工厂类，类名中 ThreadLocal 是本地线程的意思，而 ThreadLocal 最终还是使用的是 JVM 内存。
- jcache，使用的是 JCacheFactory 工厂类，是提供 javax-spi 缓存实例的工厂类，既然是一种 spi 机制，可以接入很多自制的开源框架。
- expiring，使用的是 ExpiringCacheFactory 工厂类，内部的 ExpiringCache 中还是使用的 Map 数据结构来存储数据，仍然使用的是 JVM 内存。

#### 业务缓存的缺点

1. 大对象与用户进行笛卡尔积的容量很容易撑爆内存
2. 服务器掉电或宕机容易丢失数据
3. 分布式环境中缓存的一致性问题不但增加了系统的实现复杂度，而且还容易引发各种数据不一致的业务问题。

#### 缓存需要解决的问题

1. 应用内存限制
2. 缓存刷新时间
3. 请求QPS,会不会引发缓存雪崩、穿透、击穿三大效应

#### 应用场景

1. 多次查询变化差异较小的话，可以按照一定的维度缓存起来，减少访问数据库的次数，为数据库减压
2. 对于一些聚合的业务逻辑，执行时间过长或调用次数太多，而又可以容忍一段时间内数据的差异性
3. ...


## 课程地址

[08｜缓存操作：如何为接口优雅地提供缓存功能？](https://time.geekbang.org/column/article/613346)
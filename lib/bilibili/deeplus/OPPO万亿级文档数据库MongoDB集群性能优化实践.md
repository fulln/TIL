---
dg-publish: true
title: # OPPO万亿级文档数据库MongoDB集群性能优化实践
createTime: 2023-09-03 11:57  
---
# OPPO万亿级文档数据库MongoDB集群性能优化实践
### 解决问题
#### 1. 解决核心抖动

#### 2. MongoDB 用户群技术分享

### 国内对mongoDB误解
1. 丢数据
2.  不安全，mongo被黑客攻击
3. DBA 吐槽mongoDb太难维护
	1. 国内大部分用的mysql，分布式集群多分片，状态导致国内维护难度高
	2. mongodb 资料相对欠缺
### mongo机房多活方案

#### 社区双向同步方案
![[Pasted image 20230903182030.png]]

#### 同城3机房多活方案

![[Pasted image 20230903182249.png]]

#### 同城2机房多活方案
![[Pasted image 20230903182656.png]]

#### 异地3机房多活-解决跨机房写
![[Pasted image 20230903182938.png]]

### mongodb默认线程模型

1. listener 线程负责接受所有客户端连接
2. listener 线程每收到一个新的客户端连接就创建一个线程，只负责处理该连接请求。

##### 缺陷
1. 一个链接创建一个线程，如果10w个链接，需要10w个线程， 系统负责，内存消耗也会很多
2. 链接关闭的时候， 销毁，创建进一步增加负载


#### mongodb默认线程模型-单队列方式
![[Pasted image 20230903183640.png]]
1. 模型把一次请求转成了多个任务： mongdb读操作，db数据访问
2. 任务入列到全局队列。线程池中任务从队列中获取任务执行
3. 同一个请求访问拆分到多个任务，一般一个请求通过递归来保证同一个线程处理： 多个线程由同一个线程处理
4. 任务太多，系统压力大，线程池中线程数动态增加；当任务减少，线程池中线程数动态减少

##### 网络模型缺陷
1. 获取任务执行，有全局锁竞争，会成为系统瓶颈
#### mongodb默认线程模型-多队列方式
实现难度不大，可以考虑自行实现

![[Pasted image 20230903184112.png]]


### 并行迁移实践优化

![[Pasted image 20230903185234.png]]

##### 执行步骤

1. configServe master 选出需要迁移的块，一般为S=min(M,N),m为极群数，n为需要扩容的数
2. config.locks 表中获取id = test 这条记录对应的分布式锁；上锁。
3. 异步通知需要迁移的分片开始迁移
4. 等待S个chunk迁移完成
5. 迁移完成后解锁
6. 迁移完成后延时10s
7. 重复1-6
##### 瓶颈
1. 获取分布式锁时间太长，原因： config.locks 表中的锁可能被其他操作锁住
	1. 避免其他操作占用，比如关闭autoSplite 功能，or 调大chunkSize
2. configServer 异步通知分片迁移，任意一个chunk迁移慢都会拖累迁移过程
	1. 不把多个分片迁移放到同一个逻辑，而是放到各个逻辑
3. 迁移完成后，需要10s的延迟。
	1. 延时支持可配置，动态调整
### 性能优化案例
1. 百万级高并发 mongodb 集群性能数十倍提升优化实践案例 
	1. 线程模型改成动态线程模型，一个线程可以处理多个用户请求
	2. 磁盘io，一会0，一会100，tps 有0现象。 
		1. cachesize 调整小优化
			1. 减少checkpoint刷增数据时数据量。减少磁盘io跟不上客户端写入速度导致持续io为0的问题
				1. 默认配置： checkpoint=(wait=60,log_size=2GB)
				2. 优化后配置： checkpoint=(wait=25 ,log_size= 1 GB）
			2. 预留部分内存给pageCahce，避免内存不足引起的阻塞问题
		2. 禁用enableMajorReadConcern.
	3. 存储引擎优化调优：
		1. 为了进一步减缓时延尖刺，我们继续在之前基础上对存储引擎调优，训整后配置如下：eviction dirty_trigger: 30％ ，evict_threads min: 12, evict.threads max:18,checkpoint=(wait=20,Iog_sIze= 1 GB)
![[Pasted image 20230903203222.png]]

2. 千亿级核心元数据 mongodb 集群性能数倍提升优化实践案例 
	1. 部署使用优化
		1. 预分片，写入负载均衡
		2. WriteConcern，写入大部分节点成功才返回ok
		3. 读写分离，读从优先
	2. cache淘汰策略优先
	3. checkPoint优化
	4. system.session 优化
		![[Pasted image 20230903205841.png]]
	5.  tcmalloc 内存优化
		![[Pasted image 20230903210227.png]]

3. 万亿级数据量 mongodb 集群性能数十倍提升视化实践
	1. 存储模型优化
		![[Pasted image 20230903210656.png]]
	 解决方案： 把相同的characteristic 特征的数据合并到一条，减少io操作次数，整个读写有近百倍提升
	2. group id 一直在同一个磁盘，导致io负载变高。 打散为hash进行存储
4. 千亿级数据迁移mongo，拷贝数据文件
### 如何实现mongdb 和sql融合
1. mongos 代理加mongodb协议和sql转换支持。用最小化开发成本满足sql需求
# 地址

https://www.bilibili.com/video/BV1S94y1z7Nz
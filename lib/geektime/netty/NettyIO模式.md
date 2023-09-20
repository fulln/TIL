---
dg-publish: true
title: NettyIO模式
createTime: 2023-09-20 23:36
tags:
  - netty
  - io多路复用
  - java
---
## netty 怎么切换io模式

### 经典3种io模式

1. BIO 阻塞
2. NIO 非阻塞io
3. AIO 异步io

阻塞和非阻塞的区别在于是否等待，同步与异步区别是自己去读还是回调给程序

### Netty对io的支持

1. 为啥只支持nio
	1. 连接数高，效率低
2. 为什么不支持AIO
	1. windows 很少做服务器
	2. linux下aio 不够成熟，aio提升性能不明显

#### 多种nio实现
![[attachment/Pasted image 20230920234226.png]]

1. 实现的更好
	1. netty 边缘触发和水平触发可切换
	2. netty实现的垃圾回收更少

### NIO一定优于BIO么

不见得，bio代码简单，并发度低，bio性能不输于NIO

### netty源码级支持

1. NioLoogGrop
2. NioEventLoop

# 地址

此文章为9月day20 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100036701-147214》
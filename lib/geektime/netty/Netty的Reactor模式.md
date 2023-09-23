---
dg-publish: true
title: Netty的Reactor模式
createTime: 2023-09-23 23:06
tags:
  - netty
---
# Netty的Reactor模式

Reactor的3种版本

1. reactor 单线程
2. reactor 多线程
3.  主从reactor 多线程

![[attachment/Pasted image 20230924000327.png]]

### BIO 的模式
![[attachment/Pasted image 20230924000429.png]]

### 单线程模型
![[attachment/Pasted image 20230924000500.png]]

### 多线程版本

![[attachment/Pasted image 20230924000533.png]]

### 主从线程版本
![[attachment/Pasted image 20230924000611.png]]

### netty 怎么支持的reactor模式

将serverSocketChannel 绑定到BossGroup，ScoketChannel绑定到ChildGroup
### mainReactor 只有1个线程
dobind 绑定一个地址和端口，只会调用一次。
### childGroup怎么选出的
2种模式进行选取，普通就是用hash值取模，高级就是用2的次幂获取
### 怎么跨平台

使用spi 赋值给provider，创建跨平台不同的provide。









# 地址

此文章为9月day23 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100036701-147216》
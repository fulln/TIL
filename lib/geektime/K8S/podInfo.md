---
dg-publish: true
title: 深入解析Pod对象（一）：基本概念
createTime: 2023-09-10 23:54
tags:
  - k8s
---
# 深入解析Pod对象（一）：基本概念

Pod，而不是容器，才是 Kubernetes 项目中的最小编排单位。将这个设计落实到 API 对象上，容器（Container）就成了 Pod 属性里的一个普通的字段

Pod 看成传统环境里的“机器”、把容器看作是运行在这个“机器”里的“用户程序”，那么很多关于 Pod 对象的设计就非常容易理解了。



# 地址

此文章为9月day10 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/40366》
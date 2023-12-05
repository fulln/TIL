---
dg-publish: true
title: SystemDesignInterview
createTime: 2023-10-20 18:24
tags:
  - 系统设计
  - PDF阅读
---
# SystemDesignInterview

## SCALE FROM ZERO TO MILLIONS OF USERS

> Non-relational databases might be the right choice if: 
> • Your application requires super-low latency. 
> • Your data are unstructured, or you do not have any relational data. 
> • You only need to serialize and deserialize data (JSON, XML, YAML, etc.). 
> • You need to store a massive amount of data.

[[attachment/System Design Interview An Insider’s Guide by Alex Xu (z-lib.org).pdf#page=8&selection=21,11,25,45|System Design Interview An Insider’s Guide by Alex Xu (z-lib.org), page 8]]

## 横向扩展 VS 纵向扩展

纵向扩展的问题:
> it comes with serious limitations. 
>  • Vertical scaling has a hard limit. It is impossible to add unlimited CPU and memory to a single server. 
>  • Vertical scaling does not have failover and redundancy. If one server goes down, the website/app goes down with it completely.

[[attachment/System Design Interview An Insider’s Guide by Alex Xu (z-lib.org).pdf#page=9&selection=6,35,10,41|System Design Interview An Insider’s Guide by Alex Xu (z-lib.org), page 9]]

## 负载均衡



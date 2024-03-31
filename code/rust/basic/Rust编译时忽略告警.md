---
dg-publish: true
title: Rust编译时忽略告警
createTime: 2024-01-19 15:49
tags:
  - rust
  - 命令行编译
---
## 忽略告警

### 1. 添加注解
在需要忽略的方法上添加注解:  `#[allow(dead_code)]`  即可忽略
### 2. 变量前添加_   
在需要忽略的变量上添加前缀_ 即可忽略
### 3. 添加启动参数
---
dg-publish: true
title: wget下载跳过https
createTime: 2023-09-09 19:27
tags:
  - shell
  - wget
---
# wget 下载https链接时跳过ca认证

在`wget`下载时添加请求参数` --no-check-certificate -qO`, 这样就跳过认证了
#### demo
> wget --no-check-certificate -qO - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
#### 修改后
> wget  --no-check-certificate -qO  https://apt.releases.hashicorp.com/gpg 
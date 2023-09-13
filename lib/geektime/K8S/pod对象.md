---
dg-publish: true
title: pod对象使用进阶
createTime: 2023-09-13 00:39
tags:
  - k8s
---
# 15 | 深入解析Pod对象（二）：使用进阶

作为 Kubernetes 项目里最核心的编排对象，Pod 携带的信息非常丰富。其中，资源定义（比如 CPU、内存等），以及调度相关的字段

一种特殊的 Volume，叫作 Projected Volume，你可以把它翻译为“投射数据卷”。

> 在 Kubernetes 中，有几种特殊的 Volume，它们存在的意义不是为了存放容器里的数据，也不是用来进行容器和宿主机之间的数据交换。这些特殊 Volume 的作用，是为容器提供预先定义好的数据。所以，从容器的角度来看，这些 Volume 里的信息就是仿佛是**被 Kubernetes“投射”（Project）进入容器当中的**。这正是 Projected Volume 的含义。

*Kubernetes 支持的 Projected Volume 一共有四种：*

1. Secret；
2. ConfigMap；
3. Downward API；
4. ServiceAccountToken。

### Secret
帮你把 Pod 想要访问的加密数据，存放到 Etcd 中。然后，你就可以通过在 Pod 的容器里挂载 Volume 的方式，访问到这些 Secret 里保存的信息了。

Secret 最典型的使用场景，莫过于存放数据库的 Credential 信息

```xml
apiVersion: v1
kind: Pod
metadata:
	name: test-projected-volume
spec:
	containers:
	- name: test-secret-volume
		image: busybox
		args:
		- sleep
		- "86400"
		volumeMounts:
		- name: mysql-cred
			mountPath: "/projected-volume"
			readOnly: true
	volumes:
	- name: mysql-cred
	projected:
		sources:
		- secret:
			name: user
		- secret:
			name: pass
```

它声明挂载的 Volume，并不是常见的 emptyDir 或者 hostPath 类型，而是 projected 类型。而这个 Volume 的数据来源（sources），则是名为 user 和 pass 的 Secret 对象，分别对应的是数据库的用户名和密码。

> 像这样通过挂载方式进入到容器里的 Secret，一旦其对应的 Etcd 里的数据被更新，这些 Volume 里的文件内容，同样也会被更新。其实，**这是 kubelet 组件在定时维护这些 Volume。**






# 地址 

此文章为9月day13 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/40466》
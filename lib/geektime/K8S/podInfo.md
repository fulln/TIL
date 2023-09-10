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

##  Pod 中几个重要字段的含义和用法

```yaml
apiVersion: v1
kind: Pod
...
spec:
	nodeSelector:
		disktype: ssd
```

1. **NodeSelector：是一个供用户将 Pod 与 Node 进行绑定的字段**，意味着这个 Pod 永远只能运行在携带了“disktype: ssd”标签（Label）的节点上；否则，它将调度失败。

2. **NodeName**：一旦 Pod 的这个字段被赋值，Kubernetes 项目就会被认为这个 Pod 已经经过了调度，调度的结果就是赋值的节点名字。
3. **HostAliases：定义了 Pod 的 hosts 文件（比如 /etc/hosts）里的内容**，
```yaml
apiVersion: v1
kind: Pod
...
spec:
	hostAliases:
	- ip: "10.1.2.3"
	  hostnames:
	  - "foo.remote"
	  - "bar.remote"
		...
```

这个 Pod 启动后，/etc/hosts 文件的内容将如下所示：
```yaml
cat /etc/hosts
# Kubernetes-managed hosts file.
127.0.0.1 localhost
...
10.244.135.10 hostaliases-pod
10.1.2.3 foo.remote
10.1.2.3 bar.remote
```

除了上述跟“机器”相关的配置外，你可能也会发现，**凡是跟容器的 Linux Namespace 相关的属性，也一定是 Pod 级别的**。这个原因也很容易理解：Pod 的设计，就是要让它里面的容器尽可能多地共享 Linux Namespace，仅保留必要的隔离和限制能力。这样，Pod 模拟出的效果，就跟虚拟机里程序间的关系非常类似了。

```yaml
apiVersion: v1
kind: Pod
metadata:
	name: nginx
spec:
	shareProcessNamespace: true
	containers:
	- name: nginx
	  image: nginx
	- name: shell
	  image: busybox
	  stdin: true
	  tty: true
```

意味着这个 Pod 里的容器要共享 PID Namespace。

**tty 和 stdin**。在 Pod 的 YAML 文件里声明开启它们俩，其实等同于设置了 docker run 里的 -it（-i 即 stdin，-t 即 tty）参数。

这个 Pod 被创建后，你就可以使用 shell 容器的 tty 跟这个容器进行交互了
`kubectl create -f nginx.yaml`
然后执行
`kubectl attach -it nginx -c shell`

**凡是 Pod 中的容器要共享宿主机的 Namespace，也一定是 Pod 级别的定义**
```yaml
apiVersion: v1
kind: Pod
metadata:
	name: nginx
spec:
	hostNetwork: true
	hostIPC: true
	hostPID: true
	containers:
	- name: nginx
	  image: nginx
	- name: shell
	  image: busybox
	  stdin: true
	  tty: true
```

定义了共享宿主机的 Network、IPC 和 PID Namespace。这就意味着，这个 Pod 里的所有容器，会直接使用宿主机的网络、直接与宿主机进行 IPC 通信、看到宿主机里正在运行的所有进程。

Pod 里最重要的字段当属“Containers”了。而在上一篇文章中，我还介绍过“Init Containers”。其实，这两个字段都属于 Pod 对容器的定义，内容也完全相同，只是 Init Containers 的生命周期，会先于所有的 Containers，并且严格按照定义的顺序执行。

> Kubernetes 项目中对 Container 的定义，和 Docker 相比并没有什么太大区别。我在前面的容器技术概念入门系列文章中，和你分享的 Image（镜像）、Command（启动命令）、workingDir（容器的工作目录）、Ports（容器要开发的端口），以及 volumeMounts（容器要挂载的 Volume）都是构成 Kubernetes 项目中 Container 的主要字段

#### 额外的属性

1. **ImagePullPolicy 字段**。它定义了镜像拉取的策略。而它之所以是一个 Container 级别的属性，是因为容器镜像本来就是 Container 定义中的一部分。ImagePullPolicy 的值默认是 Always，即每次创建 Pod 都重新拉取一次镜像。另外，当容器的镜像是类似于 nginx 或者 nginx:latest 这样的名字时，ImagePullPolicy 也会被认为 Always。
2. **Lifecycle 字段**。它定义的是 Container Lifecycle Hooks。顾名思义，Container Lifecycle Hooks 的作用，是在容器状态发生变化时触发一系列“钩子”。
```
apiVersion: v1
kind: Pod
metadata:
	name: lifecycle-demo
spec:
	containers:
	- name: lifecycle-demo-container
	image: nginx
	lifecycle:
		postStart:
			exec:
				command: ["/bin/sh", "-c", "echo Hello from the postStart handler > /usr/share/message"]
		preStop:
			exec:
				command: ["/usr/sbin/nginx","-s","quit"]
```

### pod 在k8s中的生命周期

1. Pending。这个状态意味着，Pod 的 YAML 文件已经提交给了 Kubernetes，API 对象已经被创建并保存在 Etcd 当中。但是，这个 Pod 里有些容器因为某种原因而不能被顺利创建。比如，调度不成功。
    
2. Running。这个状态下，Pod 已经调度成功，跟一个具体的节点绑定。它包含的容器都已经创建成功，并且至少有一个正在运行中。
    
3. Succeeded。这个状态意味着，Pod 里的所有容器都正常运行完毕，并且已经退出了。这种情况在运行一次性任务时最为常见。
    
4. Failed。这个状态下，Pod 里至少有一个容器以不正常的状态（非 0 的返回码）退出。这个状态的出现，意味着你得想办法 Debug 这个容器的应用，比如查看 Pod 的 Events 和日志。
    
5. Unknown。这是一个异常状态，意味着 Pod 的状态不能持续地被 kubelet 汇报给 kube-apiserver，这很有可能是主从节点（Master 和 Kubelet）间的通信出现了问题。


# 地址

此文章为9月day10 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/40366》
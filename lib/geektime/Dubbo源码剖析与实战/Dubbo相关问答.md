#java #dubbo #极客时间 

## 高频面试题
### 1. Dubbo 的主要节点角色有哪些？分别是干什么用的？
- Container：服务运行容器，为服务的稳定运行提供运行环境。
- Provider：提供方，暴露接口提供服务。
- Consumer：消费方，调用已暴露的接口。
- Registry：注册中心，管理注册的服务与接口。
- Monitor：监控中心，统计服务调用次数和调用时间。

### 2. Dubbo3.x 提供方注册有哪几种方式，怎么设置？消费方订阅又有哪几种方式，又怎么设置？

1. 注册方式：dubbo.application.register-mode

- interface：只接口级注册。
- instance：只应用级注册。
- all：接口级注册、应用级注册都会存在，同时也是默认值。

2. 订阅模式： dubbo.application.register-mode

- FORCE_INTERFACE：只订阅消费接口级信息。
- APPLICATION_FIRST：注册中心有应用级注册信息则订阅应用级信息，否则订阅接口级信息，起到了智能决策来兼容过渡方案。
- FORCE_APPLICATION：只订阅应用级信息。

### Dubbo 有哪些容错策略以及作用是什么？

![[Pasted image 20230220231638.png]]

### Dubbo 通过 RpcContext 开启了异步之后，是怎么衔接父子线程的上下文信息的？
1. RpcContext 通过调用 startAsync 方法开启异步模式，
2. 然后在另外的线程中采用  asyncContext.signalContextSwitch 方法来同步父线程的上下文信息，
3. 通过 asyncContext.write 写入到异步线程的上下文信息中

### 泛化调用编写代码的关键步骤是怎样的？

1. 明确 4 个维度的参数，分别是：接口类名、接口方法名、接口方法参数类名、业务请求参数。
2. 接口类名创建 ReferenceConfig 对象，设置 generic = true 属性，调用 referenceConfig.get 拿到 genericService 泛化对象。
3. 将接口方法名、接口方法参数类名、业务请求参数，传入 genericService.$invoke 方法中，即可拿到响应对象

### 点点直连有该怎么设置？

1. `<dubbo:reference url="dubbo://192.168.0.6:20884" />`
2. `@DubboReference(url = "dubbo://192.168.0.6:20884")`
3. `-Ddubbo.reference.com.hmily.dubbo.api.UserQueryFacade.url=dubbo://192.168.0.6:20884`
4. `dubbo.reference.com.hmily.dubbo.api.UserQueryFacade.url=dubbo://192.168.0.6:20884`

## 地址

此文章为2月day14 学习笔记，内容来源于极客时间《[加餐一｜中小厂高频面试：基础式的CRUD属性你清楚么？ (geekbang.org)](https://time.geekbang.org/column/article/625413)》
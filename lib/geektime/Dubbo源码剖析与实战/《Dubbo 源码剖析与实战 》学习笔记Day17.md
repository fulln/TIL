---
dg-publish: true
---

#java #dubbo #极客时间 

## 课程内容

### dubbo& spring

统一调用封装方法

#### interface
基本结构都是请求对象组装、远程调用、返参数据的判断与转换。

##### 封装
把相似流程中的变化因素提为变量，涉及以下变量

1. 下游的接口类名、方法名、方法入参类名是变量因素。
2. 消费方接口级别的 Dubbo 参数属性也是变量因素
3. 返参错误码的判断形式也是一个变量因素
4. 将数据转成各个调用方期望的对象类型，也是一个变量因素。

最终形成在统一的封装方法中接收四大对象，而在 具体的实现类中，最终就只需要调用统一的封装方法

##### 抽象

一段代码的流程，可以是业务流程，也可以是代码流程，还可以是调用流程，当然**本质都是一小块相对聚焦的业务逻辑的核心主干流程**，把不变的流程固化下来变成模板，然后把变化的因素交给各个调用方，意在求同存异，追求“不变”的稳定，放任“变化”的自由。

利用上面的4个点的变化，将调用流程简化。

因素 1 是下游的接口类名、方法名、方法入参类名，涉及的类可以放在类注解上，方法名、方法入参可以放在方法注解上。
因素 2 中消费方接口级别的 timeout、retries、loadbalance 等属性，也可以放在方法注解上。
因素 3 中的错误码，理论上下游提供方一个类中多个方法返回的格式应该是一样的，所以如何判断错误码的变量因素可以放在类注解上。
因素 4 中如何将下游数据类型转换为本系统的 Bean 类型，其实最终还是接口级别的事，貌似还是可以放到方法注解上。

```JAVA

@DubboFeignClient(
        remoteClass = SamplesFacade.class,
        needResultJudge = true,
        resultJudge = (remoteCodeNode = "respCode", remoteCodeSuccValueList = "000000", remoteMsgNode = "respMsg")
)
public interface SamplesFacadeClient {
    @DubboMethod(
            timeout = "5000",
            retries = "3",
            loadbalance = "random",
            remoteMethodName = "queryRemoteOrder",
            remoteMethodParamsTypeName = {"com.hmily.QueryOrderReq"}
     )
    QueryOrderResponse queryRemoteOrderInfo(QueryOrderRequest req);
}
```

##### 仿照spring扫描

从类注解、方法注解分别将变化的因素读取出来，然后构建调用下游系统的请求对象，并将请求对象传入下游系统的接口中，然后接收返参并针对错误码进行判断，最后转成自己的 Bean 对象。

#### 扫描原理机制

#####  DubboClassPathBeanDefinitionScanner

Dubbo 框架定义的扫描器，并且也继承了 ClassPathBeanDefinitionScanner 类

Dubbo 也在充分利用 Spring 自身已有的扩展特性来扫描自己需要关注的三个注解类，org.apache.dubbo.config.annotation.DubboService、org.apache.dubbo.config.annotation.Service、com.alibaba.dubbo.config.annotation.Service，然后完成 BeanDefinition 对象的创建，再完成 Proxy 代理对象的创建，最后在运行时就可以直接被拿来使用了。


## 课程地址

[13｜集成框架：框架如何与Spring有机结合？]([13｜集成框架：框架如何与Spring有机结合？ (geekbang.org)](https://time.geekbang.org/column/article/615378))
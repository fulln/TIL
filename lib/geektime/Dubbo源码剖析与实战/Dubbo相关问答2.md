#java #dubbo #极客时间 

## Dubbo常见问题与答案

### Dubbo 的事件通知怎么设置？

通过FutureFilter 过滤器设置，主要有3种设置

1. 在 invoker.invoke(invocation) 方法之前，利用 fireInvokeCallback 方法反射调用了接口配置中指定服务中的 onInvoke 方法。
2. 然后在 onResponse 响应时，处理了正常返回和异常返回的逻辑，分别调用了接口配置中指定服务中的 onReturn、onThrow 方法。
3. 最后在 onError 框架异常后，调用了接口配置中指定服务中的 onThrow 方法

### Dubbo 的参数验证是怎么设置的？

1. 一般方式，设置 validation 为 jvalidation、jvalidationNew 两种框架提供的值。
2. 特殊方式，设置 validation 为自定义校验器的类路径，并将自定义的类路径添加到 META-INF 文件夹下面的 org.apache.dubbo.validation.Validation 文件中。

相关demo
```java

@Component
public class InvokeDemoFacade {

    // 注意，@DubboReference 这里添加了 validation 属性
    @DubboReference(validation ＝ "jvalidation")
    private ValidationFacade validationFacade;
    
    // 一个简单的触发调用下游 ValidationFacade.validateUser 的方法
    public String invokeValidate(String id, String name, String sex) {
        return validationFacade.validateUser(new ValidateUserInfo(id, name, sex));
    }
}
```

### Dubbo 怎么设置缓存？缓存有哪些类似可以设置？

#### 缓存设置

1.  <dubbo:service/>、
2. <dubbo:method/>、
3. <dubbo:provider/>、
4. <dubbo:consumer/>、
5. @DubboReference、
6. @DubboService

#### 缓存类型
lru，使用的是 LruCacheFactory 工厂类，类注释上有提到使用 LruCache 缓存类来进行处理，实则背后使用的是 JVM 内存。
threadlocal，使用的是 ThreadLocalCacheFactory 工厂类，类名中 ThreadLocal 是本地线程的意思，而 ThreadLocal 最终还是使用的是 JVM 内存。
jcache，使用的是 JCacheFactory 工厂类，是提供 javax-spi 缓存实例的工厂类，既然是一种 spi 机制，可以接入很多自制的开源框架。
expiring，使用的是 ExpiringCacheFactory 工厂类，内部的 ExpiringCache 中还是使用的 Map 数据结构来存储数据，仍然使用的是 JVM 内存。

### 配置的加载顺序是怎样的？

![[Pasted image 20230221230647.png]]

#### 主要有四个层级关系。

- System Properties，最高优先级，我们一般会在启动命令中通过 JVM 的 -D 参数进行指定，图中通过 -D 参数从指定的磁盘路径加载配置，也可以从公共的 NAS 路径加载配置。
- Externalized Configuration，优先级次之，外部化配置，我们可以直接从统一的配置中心加载配置，图中就是从 Nacos 配置中心加载配置。
- API / XML / 注解，优先级再次降低，这三种应该是我们开发人员最熟悉不过的配置方式了。
- Local File，优先级最低，一般是项目中默认的一份基础配置，当什么都不配置的时候会读取。


### Dubbo 默认使用的是什么通信框架？

默认使用 Netty 作为 Dubbo 的网络通信框架。同时，Netty 也位于 Dubbo 十层模块中的第 9 层，Transport 层。

### Dubbo 的dubbo:application 、dubbo:reference 等标签，是怎么被加载到 Spring 中的？

Spring 的底层会回调 NamespaceHandler 接口的所有实现类，调用每个实现类的 parse 方法，然而 DubboNamespaceHandler 也就是在这个 parse 方法中完成了配置的解析，并转为 Spring 的 bean 对象


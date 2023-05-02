---
dg-publish: true
---

#java #dubbo #极客时间 

##  加餐｜大厂高频面试：底层的源码逻辑知多少？

### Dubbo 源码分层模块是怎样的？

![[《Dubbo 源码剖析与实战 》学习笔记Day16#模块化流程]]

### Dubbo 如何扫描含有 @DubboService 这种注解的类？

Dubbo 利用了一个 DubboClassPathBeanDefinitionScanner 类继承了 ClassPathBeanDefinitionScanner，充分利用 Spring 自身已有的扩展特性来扫描自己需要关注的三个注解类，org.apache.dubbo.config.annotation.DubboService、org.apache.dubbo.config.annotation.Service、com.alibaba.dubbo.config.annotation.Service，然后完成 BeanDefinition 对象的创建。


在 BeanDefinition 对象的实例化完成后，在容器触发刷新的事件过程中，通过回调了 ServiceConfig 的 export 方法完成了服务导出，即完成 Proxy 代理对象的创建，最后在运行时就可以直接被拿来使用了。


### Dubbo SPI 解决了 JDK SPI 的什么问题？

DK SPI 使用一次，就会一次性实例化所有实现类。为了弥补我们分析的 JDK SPI 的不足，Dubbo 也定义出了自己的一套 SPI 机制逻辑，既要通过 O(1) 的时间复杂度来获取指定的实例对象，还要控制缓存创建出来的对象，做到按需加载获取指定实现类。

Dubbo SPI 在实现的过程中，采用了两种方式来优化。

- 方式一，增加缓存，来降低磁盘 IO 访问以及减少对象的生成。
- 方式二，使用 Map 的 hash 查找，来提升检索指定实现类的性能。
 
通过两种方式的优化后，在面对大量高频调用时，JDK SPI 可能会出现磁盘 IO 吞吐下降、大量对象产生和查询指定实现类的 O(n) 复杂度等问题，而 Dubbo SPI 采用缓存 +Map 的组合方式更加友好地避免了这些情况，即使大量调用，也问题不大。

### 简要描述下 Dubbo SPI 与 Spring SPI 的加载原理？

Dubbo SPI 的核心加载原理，就是加载了以下三个资源路径下的文件内容，资源分别为。

- META-INF/dubbo/internal/
- META-INF/dubbo/
- META-INF/services/
 
我们自己设计的 SPI 接口，放到这 3 个资源路径下都可以，不过从路径的名称上可以看出，

1. META-INF/dubbo/internal/ 存放的是 Dubbo 内置的一些扩展点，
2. META-INF/services/ 存放的是 Dubbo 自身的一些业务逻辑所需要的一些扩展点，
3. META-INF/dubbo/ 存放的是上层业务系统自身的一些定制 Dubbo 的相关扩展点。
 
而相比于 JDK 原生的 SPI，Spring 中的 SPI 功能也很强大，主是通过 org.springframework.core.io.support.SpringFactoriesLoader#loadFactories 方法读取所有 jar 包的`META-INF/spring.factories`资源文件，并从文件中读取一堆的类似 EnableAutoConfiguration 标识的类路径，把这些类创建对应的 Spring Bean 对象注入到容器中，就完成了 SpringBoot 的自动装配。

### LinkedHashMap 可以设计成 LRU 么？

LRU2Cache 缓存类，它的底层实现原理就是继承了 LinkedHashMap 的类，然后重写了父类 LinkedHashMap 中的 removeEldestEntry 方法，当 LRU2Cache 存储的数据个数大于设置的容量后，会删除最先存储的数据，让最新的数据能够保存进来。

```java

// LRU2Cache 的带参构造方法，在 LruCache 构造方法中，默认传入的大小是 1000                  
org.apache.dubbo.common.utils.LRU2Cache#LRU2Cache(int)
public LRU2Cache(int maxCapacity) {
    super(16, DEFAULT_LOAD_FACTOR, true);
    this.maxCapacity = maxCapacity;
    this.preCache = new PreCache<>(maxCapacity);
}
// 若继续放数据时，若发现现有数据个数大于 maxCapacity 最大容量的话
// 则会考虑抛弃掉最古老的一个，也就是会抛弃最早进入缓存的那个对象
@Override
protected boolean removeEldestEntry(java.util.Map.Entry<K, V> eldest) {
    return size() > maxCapacity;
}
                  ↓
// JDK 中的 LinkedHashMap 源码在发生节点插入后
// 给了子类一个扩展删除最旧数据的机制                   
java.util.LinkedHashMap#afterNodeInsertion
void afterNodeInsertion(boolean evict) { // possibly remove eldest
    LinkedHashMap.Entry<K,V> first;
    if (evict && (first = head) != null && removeEldestEntry(first)) {
        K key = first.key;
        removeNode(hash(key), key, null, false, true);
    }
}
```

### 利用 Dubbo 框架怎么来做分布式限流呢？

控制流量的三个关键环节。

- 第一，寻找请求流经的必经之路，并在必经之路上找到可扩展的接口。
- 第二，找到该接口的众多实现类，研究在触发调用的入口可以拿到哪些数据，再研究关于方法的入参数据、方法本身信息以及方法归属类的信息可以通过哪些 API 拿到。
- 第三，根据限流的核心计算模块，逐渐横向扩展，从单个方法到多个方法，从单个服务到多个服务，从单个节点到集群节点，尽可能周全地考虑通用处理方式，同时站在使用者的角度，做到简单易用的效果。

### Wrapper 是怎么降低调用开销的？

Wrapper 代理类 最终调用了 getWrapper 方法来生成一个代理类。 

- 以源对象的类属性为维度，与生成的代理类建立缓存映射关系，避免频繁创建代理类影响性能。
- 生成了一个继承 Wrapper 的动态类，并且暴露了一个公有 invokeMethod 方法来调用源对象的方法。
- 在 invokeMethod 方法中，通过生成的 if…else 逻辑代码来识别调用源对象的不同方法。

Wrapper 降低开销的主要有 2 个关键要素的原因。

- 原因一，生成了代理类缓存起来，避免频繁创建对象。
- 原因二，代理类中的逻辑，是通过 if…else 的普通代码进行了强转操作，转为原始对象后继续调用方法，而不是采用反射方式来调用方法的。

## 地址

此文章为2月day16 学习笔记，内容来源于极客时间《[加餐｜大厂高频面试：底层的源码逻辑知多少？ (geekbang.org)](https://time.geekbang.org/column/article/625429)》
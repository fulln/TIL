---
dg-publish: true
---

#java #极客时间 #dubbo 

##  注册扩展：如何统一添加注册信息？

网关调用后端对应IP时，可以通过手动配IP的形式

```java

<dubbo:reference url="dubbo://[机器IP结点]:[机器IP提供Dubbo服务的端口]" />
或者
@DubboReference(url = "dubbo://[机器IP结点]:[机器IP提供Dubbo服务的端口]")
```

场景不同，选择的方法也不同

1. 若项目小而轻量级，通过指定 url 属性不失为一种最快的方式
2. 变成可配置化形式，就不必再为了修改代码、打包和部署而烦恼了。

在[[《Dubbo 源码剖析与实战 》学习笔记Day15#配置加载顺序]] 中，也提到了修改，则可以这样

```properties
///////////////////////////////////////////////////
// System Properties 层级配置
// JVM 启动命令中添加如下 -D 的这一串属性
///////////////////////////////////////////////////
-Ddubbo.reference.com.hmily.dubbo.api.UserQueryFacade.url=dubbo://192.168.0.6:20884

///////////////////////////////////////////////////
// Externalized Configuration 层级配置
// 比如外部配置文件为：dubbo.properties
///////////////////////////////////////////////////
dubbo.reference.com.hmily.dubbo.api.UserQueryFacade.url=dubbo://192.168.0.6:20884
```

如果需要自动识别ip，则需要扩展下注册
> 在抽象的时候，我们可以先梳理整个功能的流程，然后反复琢磨每个步骤，看看是否能撕开一个口子做扩展，通过少量的代码编写来完成抽象的能力。

#### dubbo 调用框架
![[Pasted image 20230215224323.png]]

在Cluster层次，有个故障转移策略，可以通过重试机拿到多个invoke对象去调用，可以在invoker对象中添加自定义的值，可以写在urlParam里面

**invoker对象中的urlParam属性，在消费方的首次订阅和后续节点变更时，都会从 ZooKeeper 拉取最新的数据**

在[[DUBBO发布流程#主要export方法]]中，可以在这方法里面的`getRegistry`对url进行处理，主要流程为

```JAVA

///////////////////////////////////////////////////
// org.apache.dubbo.registry.integration.RegistryProtocol#getRegistry
// 通过注册中心地址来获取 Registry 实现类
///////////////////////////////////////////////////
/**
 * Get an instance of registry based on the address of invoker
 *
 * @param registryUrl
 * @return
 */
protected Registry getRegistry(final URL registryUrl) {
    // 获取 RegistryFactory 接口的自适应扩展点代理对象
    // 主要是调用了 getAdaptiveExtension 方法即可知道拿到了一个代理对象
    RegistryFactory registryFactory = ScopeModelUtil.getExtensionLoader(RegistryFactory.class, registryUrl.getScopeModel()).getAdaptiveExtension();
    
    // 通过代理对象获取入参指定扩展点的实现类
    // 默认逻辑是从 address 注册中心地址（zookeeper://127.0.0.1:2181）中根据 zookeeper 来找到对应的实现类
    // 到时候就只需要模仿 ZookeeperRegistry 就行 
    return registryFactory.getRegistry(registryUrl);
}
```

可以看到，如果想达到对应效果

1. 复制了 ZookeeperRegistryFactory 的源码，并改了个名字为路由编码注册工厂（RouteNoZkRegistryFactory），其中，重写了 createRegistry 方法，返回了自己创建的路由编码注册器（RouteNoZkRegistry）。
2. 在路由编码注册器（RouteNoZkRegistry）中，主要继承了已有的 ZookeeperRegistry 类，并重写了注册与注销的方法，在两个方法中都额外添加了一个新字段 routeNo 属性，属性值为当前 IP 机器易于识别的简单别名。
3. 把路由编码注册工厂（RouteNoZkRegistryFactory）添加到资源目录对应的 SPI 接口文件中（/META-INF/dubbo/org.apache.dubbo.registry.RegistryFactory）。
4. 在设置注册中心地址时，把已有的 zookeeper 替换为 routenoregistry。

#### 应用场景

 第一，添加路由标识，统一在消费方进行动态路由，以选择正确标识对应的 IP 地址进行远程调用。

第二，添加系统英文名，统一向注册信息中补齐接口归属的系统英文名，当排查一些某些接口的问题时，可以迅速从注册中心查看接口归属的系统英文名。

第三，添加环境信息，统一从请求的入口处，控制产线不同环境的流量比例，主要是控制少量流量对一些新功能进行内测验证。


## 地址

此文章为2月day9 学习笔记，内容来源于极客时间《[25｜注册扩展：如何统一添加注册信息？ (geekbang.org)](https://time.geekbang.org/column/article/625388)》，推荐该课程
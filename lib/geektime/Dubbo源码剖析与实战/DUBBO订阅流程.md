---
dg-publish: true
---

#java #极客时间 #dubbo 

## 课程内容

### DUBBO 订阅流程

订阅方式：
1. <dubbo:reference/>
2. @DubboReference

#### 与`@DubboService`的对比

作用域，@DubboService 是作用于提供方的，而 @DubboReference 是作用于消费方的；
类的名称，@DubboService 会落到 ServiceConfig 中进行导出，而 @DubboReference 会落到 ReferenceConfig 中进行引用；
辐射功能，ServiceConfig 中涵盖了本地导出和远程导出两个重要的分支逻辑，

#### ReferenceConfig的get方法

```java

///////////////////////////////////////////////////
// org.apache.dubbo.config.ReferenceConfig#get
// 引用提供方的核心方法
///////////////////////////////////////////////////
@Override
public T get() {
    // 省略其他部分代码...
    if (ref == null) {
        // ensure start module, compatible with old api usage
        getScopeModel().getDeployer().start();
        synchronized (this) {
            // !!!!!!!!!!!!!!!!!!!!!!!!!!!!
            // 重点关注这里
            // 如果 ref 对象为空，这就初始化一个
            // 说明引用提供方的每个接口都有着与之对应的一个 ref 对象
            if (ref == null) {
                // 初始化 ref 对象
                init();
            }
        }
    }
    return ref;
}
                  ↓
///////////////////////////////////////////////////                  
// org.apache.dubbo.config.ReferenceConfig#init
// 初始化的逻辑很多，这里就直接挑选最重要的核心逻辑，创建代理对象方法来跟踪
///////////////////////////////////////////////////
protected synchronized void init() {
    // 省略其他部分代码...
    // 这里省略了一大堆的引用提供方所设置的一些参数
    // 就是那些设置在 @DubboReference 注解中的配置，最终会在综合为一个 Map 对象
    // 而这个所谓的 Map 对象其实就是 referenceParameters 这个引用参数对象
    
    // 根据引用参数创建代理对象
    ref = createProxy(referenceParameters);
    
    // 省略其他部分代码...
}
                  ↓
///////////////////////////////////////////////////                  
// org.apache.dubbo.config.ReferenceConfig#createProxy
// 创建代理对象的核心逻辑：injvm引用 + 远程引用 + 生成代理对象
///////////////////////////////////////////////////
private T createProxy(Map<String, String> referenceParameters) {
    // 判断是不是按照 injvm 协议进行引用
    if (shouldJvmRefer(referenceParameters)) {
        createInvokerForLocal(referenceParameters);
    } 
    // 能来到这里，说明不是 injvm 协议，那就按照正常的协议进行引用
    else {
        urls.clear();
        // url 不为空，说明有单独进行点点直连的诉求
        if (StringUtils.isNotEmpty(url)) {
            // user specified URL, could be peer-to-peer address, or register center's address.
            // 将填写的 url 字符串内容解析为 URL 对象，并添加到 urls 集合中去
            // 这里有个小细节就是，若解析的过程中发现是注册中心地址的话
            // 那么就会将服务引用的 referenceParameters 整体信息归到注册中心地址的 "refer" 属性上
            // 就像服务导出时一样，将服务接口的整体信息归到注册中心地址的 "export" 属性上
            parseUrl(referenceParameters);
        } else {
            // if protocols not in jvm checkRegistry
            // 如果协议不是 injvm 的话，那么这里还会再次获取最新的注册中心地址
            // 如果最后发现 urls 中的集合为空的话，那么就会抛出异常
            // 目的就是检查一定得有 urls 内容，否则根本不用走后续的引用逻辑了
            if (!"injvm".equalsIgnoreCase(getProtocol())) {
                aggregateUrlFromRegistry(referenceParameters);
            }
        }
        // 为远程引用创建 invoker 对象
        createInvokerForRemote();
    }
    
    // 省略其他部分代码...
    
    // 创建刚刚创建出来的 invoker 对象通过调用 proxyFactory.getProxy 方法包装成代理对象
    return (T) proxyFactory.getProxy(invoker, ProtocolUtils.isGeneric(generic));
}
```

###### 创建本地引用

```java

///////////////////////////////////////////////////                  
// org.apache.dubbo.config.ReferenceConfig#createInvokerForLocal
// 为本地引用创建 invoker 对象
///////////////////////////////////////////////////
private void createInvokerForLocal(Map<String, String> referenceParameters) {
    // 将引用服务的参数对象 referenceParameters、injvm 重新再次封装为一个新对象
    URL url = new ServiceConfigURL("injvm", "127.0.0.1", 0, interfaceClass.getName(), referenceParameters);
    url = url.setScopeModel(getScopeModel());
    url = url.setServiceModel(consumerModel);
    // url：injvm://127.0.0.1/com.hmilyylimh.cloud.facade.demo.DemoFacade?application=dubbo-20-subscribe-consumer&background=false&dubbo=2.0.2&interface=com.hmilyylimh.cloud.facade.demo.DemoFacade&methods=sayHello,say&pid=8632&qos.enable=false&register.ip=192.168.100.183&release=3.0.7&side=consumer&sticky=false&timestamp=1670774005173
    
    // 服务引用，返回的 invoker 对象这里也做了比较友好的命名说明
    // withFilter 其实就是想表达，即使是本地引用也有过滤器拦截那一堆的特性
    Invoker<?> withFilter = protocolSPI.refer(interfaceClass, url);
    // Local Invoke ( Support Cluster Filter / Filter )
    
    // 将 invoker 对象最终聚合为一个集群 invoker 对象
    // 从另外一个角度看的话，也就意味着 Cluster 里面是有多个 invoker 对象的
    List<Invoker<?>> invokers = new ArrayList<>();
    invokers.add(withFilter);
    invoker = Cluster.getCluster(url.getScopeModel(), "failover").join(new StaticDirectory(url, invokers), true);
}
```

主要流程和export方法差不多：

![[Pasted image 20230208225007.png]]

在调用InjvmProtocol 的接口时，就是直接在本地创建了一个 InjvmInvoker 对象而已，并且源码再次向我们证明了 export 和 refer 是成对存在的。

###### 创建远程引用

远程调用，和远程导出是成对的，就是使用了Netty绑定协议端口提供服务，然后在调用的时候也是使用的NettyClient来接收连接

```JAVA

///////////////////////////////////////////////////                  
// org.apache.dubbo.config.ReferenceConfig#createInvokerForRemote
// 为远程引用创建 invoker 对象
///////////////////////////////////////////////////
private void createInvokerForRemote() {
    // 若 urls 集合只有 1 个元素的话，则直接调用 refer 进行远程引用
    if (urls.size() == 1) {
        URL curUrl = urls.get(0);
        // 远程引用的核心代码
        invoker = protocolSPI.refer(interfaceClass, curUrl);
        if (!UrlUtils.isRegistry(curUrl)) {
            // 如果这个 curUrl 不是注册协议的话，
            // 那么就用集群扩展器包装起来
            List<Invoker<?>> invokers = new ArrayList<>();
            invokers.add(invoker);
            invoker = Cluster.getCluster(scopeModel, Cluster.DEFAULT).join(new StaticDirectory(curUrl, invokers), true);
        }
    } 
    // 能来到这里，说明 urls 有多个地址，
    // 可能有注册中心地址，也可能有服务接口引用地址
    // 反正有混合的可能性
    else {
        List<Invoker<?>> invokers = new ArrayList<>();
        URL registryUrl = null;
        // 既然 urls 有多个元素的话，那就干脆直接循环进行挨个挨个远程引用
        for (URL url : urls) {
            // For multi-registry scenarios, it is not checked whether each referInvoker is available.
            // Because this invoker may become available later.
            // 循环体中单独针对针对一个 url 进行远程引用
            invokers.add(protocolSPI.refer(interfaceClass, url));
            if (UrlUtils.isRegistry(url)) {
                // use last registry url
                registryUrl = url;
            }
        }
        // 如果循环完了之后，发现含有注册中心地址的话，
        // 那就继续用集群扩展器包装起来
        if (registryUrl != null) {
            // registry url is available
            // for multi-subscription scenario, use 'zone-aware' policy by default
            String cluster = registryUrl.getParameter(CLUSTER_KEY, ZoneAwareCluster.NAME);
            // The invoker wrap sequence would be: ZoneAwareClusterInvoker(StaticDirectory) -> FailoverClusterInvoker
            // (RegistryDirectory, routing happens here) -> Invoker
            // 集群扩展器包装 invokers 列表 
            invoker = Cluster.getCluster(registryUrl.getScopeModel(), cluster, false).join(new StaticDirectory(registryUrl, invokers), false);
        } 
        // 循环完了后若发现没有注册中心地址，
        // 那很有可能就是点点直连方式进行点对点连接
        // 于是，还是一样采用集群扩展器包装起来
        else {
            // not a registry url, must be direct invoke.
            if (CollectionUtils.isEmpty(invokers)) {
                throw new IllegalArgumentException("invokers == null");
            }
            URL curUrl = invokers.get(0).getUrl();
            String cluster = curUrl.getParameter(CLUSTER_KEY, Cluster.DEFAULT);
            // 集群扩展器包装 invokers 列表
            invoker = Cluster.getCluster(scopeModel, cluster).join(new StaticDirectory(curUrl, invokers), true);
        }
    }
}
                  ↓
///////////////////////////////////////////////////                  
// org.apache.dubbo.registry.integration.RegistryProtocol#refer
// 注册协议的引用方法，该类中还有一个 export 导出的方法，他们俩是成对存在的
///////////////////////////////////////////////////
public <T> Invoker<T> refer(Class<T> type, URL url) throws RpcException {
    // 首先一进入方法，你可以先看下入参url是个大概的什么内容
    // 入参url：registry://127.0.0.1:2181/org.apache.dubbo.registry.RegistryService?REGISTRY_CLUSTER=registryConfig&application=dubbo-20-subscribe-consumer&dubbo=2.0.2&pid=7032&qos.enable=false&registry=ZooKeeper&release=3.0.7&timestamp=1670774973194
    url = getRegistryUrl(url);
    
    // 然后经过 getRegistryUrl 方法后，又变成了什么样子
    // 结果发现协议被替换了，由 registry 协议替换成了 zookeeper 协议
    // getRegistryUrl 后的 url：zookeeper://127.0.0.1:2181/org.apache.dubbo.registry.RegistryService?REGISTRY_CLUSTER=registryConfig&application=dubbo-20-subscribe-consumer&dubbo=2.0.2&pid=7032&qos.enable=false&release=3.0.7&timestamp=1670774973194
    Registry registry = getRegistry(url);
    if (RegistryService.class.equals(type)) {
        return proxyFactory.getInvoker((T) registry, type, url);
    }
    
    // group="a,b" or group="*"
    // 这里涉及一个一个分组的概念，不过常常会和 merger 聚合参数一起使用
    Map<String, String> qs = (Map<String, String>) url.getAttribute(REFER_KEY);
    String group = qs.get(GROUP_KEY);
    if (StringUtils.isNotEmpty(group)) {
        if ((COMMA_SPLIT_PATTERN.split(group)).length > 1 || "*".equals(group)) {
            // 执行核心的 doRefer 方法
            return doRefer(Cluster.getCluster(url.getScopeModel(), MergeableCluster.NAME), registry, type, url, qs);
        }
    }
    
    // 能来到这个还是，发现最终还是调用核心的 doRefer 方法
    // 因此不管是分组聚合情况，还是普通的情况，最终重心都落到了 doRefer 方法
    Cluster cluster = Cluster.getCluster(url.getScopeModel(), qs.get(CLUSTER_KEY));
    return doRefer(cluster, registry, type, url, qs);
}
```


1. 远程引用的 urls 集合，既可以是注册中心地址，也可以多个提供方的点对点地址。
2. 不管 urls 集合的数量是一个还是多个，最终都是循环调用 refer 方法，然后累加 refer 的所有结果，最终被集群扩展器包装成了一个 invoker。
3. refer 的方法体中将注册器、集群扩展器、接口等信息全部封装到了一个 doRefer 方法中。

从 RegistryProtocol 的 doRefer 一路跟踪，最终又回到了 RegistryProtocol 的 doCreateInvoker 方法，而且从方法名也能看出是创建 invoker 对象的核心逻辑，因此远程引用的核心逻辑就落到了 doCreateInvoker 方法中

```java

///////////////////////////////////////////////////                  
// RegistryProtocol#doCreateInvoker
// 兜兜转转又回到了注册协议实现类的创建 invoker 方法来了
///////////////////////////////////////////////////
protected <T> ClusterInvoker<T> doCreateInvoker(DynamicDirectory<T> directory, Cluster cluster, Registry registry, Class<T> type) {
    directory.setRegistry(registry);
    directory.setProtocol(protocol);
    
    // all attributes of REFER_KEY
    // 这里构建了一个需要写到注册中心的地址信息
    // 之前在导出的方法中我们也看到了提供者会把服务接口的地址信息写到注册中心上
    // 结果这里同样写到注册中心上，说明只要是 dubbo 服务，不管是提供者还是消费者，
    // 最终都会把自己的提供的服务接口信息，或需要订阅的服务接口信息，都会写到注册中心去
    Map<String, String> parameters = new HashMap<>(directory.getConsumerUrl().getParameters());
    URL urlToRegistry = new ServiceConfigURL(
        parameters.get(PROTOCOL_KEY) == null ? CONSUMER : parameters.get(PROTOCOL_KEY),
        parameters.remove(REGISTER_IP_KEY),
        0,
        getPath(parameters, type),
        parameters
    );
    urlToRegistry = urlToRegistry.setScopeModel(directory.getConsumerUrl().getScopeModel());
    urlToRegistry = urlToRegistry.setServiceModel(directory.getConsumerUrl().getServiceModel());
    if (directory.isShouldRegister()) {
        // 将构建好的的 urlToRegistry 字符串内容写到注册中心去
        directory.setRegisteredConsumerUrl(urlToRegistry);
        registry.register(directory.getRegisteredConsumerUrl());
    }
    // 设置路由规则
    directory.buildRouterChain(urlToRegistry);
    // 构建订阅的地址 subscribeUrl 然后发起订阅，然后会监听注册中心的目录
    directory.subscribe(toSubscribeUrl(urlToRegistry));
    return (ClusterInvoker<T>) cluster.join(directory, true);
}
```

**doCreateInvoker 方法中主要做了两件事情：向注册中心注册了消费接口的信息、向注册中心发起了订阅及监听。**

在 doCreateInvoker 方法中主要做了两件事情：向注册中心注册了消费接口的信息、向注册中心发起了订阅及监听。在`subscribe` 中发起创建netty连接和订阅

首先是熟悉的方法名，为远程引用创建 invoker 的方法入口 createInvokerForRemote。RegistryProtocol 中创建 invoker 的核心方法 doCreateInvoker。
还未来得及进入源码一探究竟的 subscribe 接口订阅方法。
接口订阅之后来了一堆的 notify 的通知方法，并且又再次走了一遍 refer 方法，很是奇怪。
最后是 NettyClient 的 doConnect 方法。

#### 订阅

主要处理逻辑
```java

///////////////////////////////////////////////////                  
// org.apache.dubbo.registry.zookeeper.ZookeeperRegistry#doSubscribe
// 订阅的核心逻辑，读取 zk 目录下的数据，然后通知刷新内存中的数据
///////////////////////////////////////////////////
@Override
public void doSubscribe(final URL url, final NotifyListener listener) {
    try {
        checkDestroyed();
        // 因为这里用 * 号匹配，我们在真实的线上环境也不可能将服务接口配置为 * 号
        // 因此这里的 * 号逻辑暂且跳过，直接看后面的具体接口的逻辑
        if ("*".equals(url.getServiceInterface())) {
            // 省略其他部分代码...
        } 
        // 能来到这里，说明 ServiceInterface 不是 * 号
        // url.getServiceInterface() = com.hmilyylimh.cloud.facade.demo.DemoFacade
        else {
            CountDownLatch latch = new CountDownLatch(1);
            try {
                List<URL> urls = new ArrayList<>();
                // toCategoriesPath(url) 得出来的集合有以下几种：
                // 1、/dubbo/com.hmilyylimh.cloud.facade.demo.DemoFacade/providers
                // 2、/dubbo/com.hmilyylimh.cloud.facade.demo.DemoFacade/configurators
                // 3、/dubbo/com.hmilyylimh.cloud.facade.demo.DemoFacade/routers
                for (String path : toCategoriesPath(url)) {
                    ConcurrentMap<NotifyListener, ChildListener> listeners = zkListeners.computeIfAbsent(url, k -> new ConcurrentHashMap<>());
                    ChildListener zkListener = listeners.computeIfAbsent(listener, k -> new RegistryChildListenerImpl(url, path, k, latch));
                    if (zkListener instanceof RegistryChildListenerImpl) {
                        ((RegistryChildListenerImpl) zkListener).setLatch(latch);
                    }
                    // 向 zk 创建持久化目录，一种容错方式，担心目录被谁意外的干掉了
                    zkClient.create(path, false);
                    
                    // !!!!!!!!!!!!!!!!
                    // 这段逻辑很重要了，添加对 path 目录的监听，
                    // 添加监听完成后，还能拿到 path 路径下所有的信息
                    // 那就意味着监听一旦添加完成，那么就能立马获取到该 DemoFacade 接口到底有多少个提供方节点
                    List<String> children = zkClient.addChildListener(path, zkListener);
                    // 将返回的信息全部添加到 urls 集合中
                    if (children != null) {
                        urls.addAll(toUrlsWithEmpty(url, path, children));
                    }
                }
                
                // 从 zk 拿到了所有的信息后，然后调用 notify 方法
                // url.get(0) = dubbo://192.168.100.183:28200/com.hmilyylimh.cloud.facade.demo.DemoFacade?anyhost=true&application=dubbo-20-subscribe-consumer&background=false&check=false&deprecated=false&dubbo=2.0.2&dynamic=true&generic=false&interface=com.hmilyylimh.cloud.facade.demo.DemoFacade&methods=sayHello,say&register-mode=interface&release=3.0.7&side=provider
                // url.get(1) = empty://192.168.100.183/com.hmilyylimh.cloud.facade.demo.DemoFacade?application=dubbo-20-subscribe-consumer&background=false&category=configurators&dubbo=2.0.2&interface=com.hmilyylimh.cloud.facade.demo.DemoFacade&methods=sayHello,say&pid=11560&qos.enable=false&release=3.0.7&side=consumer&sticky=false&timestamp=1670846788876
                // url.get(2) = empty://192.168.100.183/com.hmilyylimh.cloud.facade.demo.DemoFacade?application=dubbo-20-subscribe-consumer&background=false&category=routers&dubbo=2.0.2&interface=com.hmilyylimh.cloud.facade.demo.DemoFacade&methods=sayHello,say&pid=11560&qos.enable=false&release=3.0.7&side=consumer&sticky=false&timestamp=1670846788876
                notify(url, listener, urls);
            } finally {
                // tells the listener to run only after the sync notification of main thread finishes.
                latch.countDown();
            }
        }
    } catch (Throwable e) {
        throw new RpcException("Failed to subscribe " + url + " to zookeeper " + getUrl() + ", cause: " + e.getMessage(), e);
    }
}
```


第一点，根据订阅的 url 信息，解析出 category 类别集合，类别除了有看到的 providers、configurators、routers，还有一个 consumers，但是因为我们目前是消费方进行订阅，解析出来的类别集合没有 consumers 也是合乎情理的。

第二点，循环为刚刚解析出来的 category 类别路径添加监听，并同时获取到类别目录下所有的信息，也就是说这里与注册中心有了通信层面的交互，拿到了注册中心关于订阅接口的所有信息。

第三点，将获取到的所有信息组装成为 urls 集合，统一调用 notify 方法刷新

**当消费方向注册中心发起接口订阅的时候，就已经拿到了该接口在注册中心的提供方信息、配置信息、路由信息。**

##### 整體流程

![[Pasted image 20230208233130.png]]


#### 推拉模式总结

dubbo 可见使用的是pull 模式

push 模式的优点是实时性强，客户端只要简单的被动接收即可。但是也容易导致消息积压，同时也加大了服务端的逻辑复杂度。

pull 模式的优点是主动权掌握在客户端自己手中，消费多少就取多少，长轮询的操作也顶多就是耗费消费方一些线程资源和网络带宽，但是，轮询间隔也得在实时性能容忍的情况下，且不会对服务端造成太大请求压力冲击。这样，客户端的逻辑就会更加复杂，反而会使得服务端简单干脆。

## 课程地址

此文章为2月day3 学习笔记，内容来源于极客时间《[20｜订阅流程：消费方是怎么知道提供方地址信息的？ (geekbang.org)](https://time.geekbang.org/column/article/621013)》，推荐该课程
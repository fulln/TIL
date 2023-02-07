#java #dubbo #极客时间 

## 内容

### dubbo 服务发布

**配置 -> 导出 -> 注册**

#### 配置

可以见`@DubboService`

1. 查看 DubboService.class。
2. 找到ServiceAnnotationType的list
```JAVA

// org.apache.dubbo.config.spring.beans.factory.annotation.ServiceAnnotationPostProcessor#scanServiceBeans
private void scanServiceBeans(Set<String> packagesToScan, BeanDefinitionRegistry registry) {
    // 省略其他部分代码...
    
    // 创建一个扫描器来扫描 Dubbo 路径下的所有 Bean 定义
    DubboClassPathBeanDefinitionScanner scanner =
            new DubboClassPathBeanDefinitionScanner(registry, environment, resourceLoader);
    // 省略其他部分代码...
    for (String packageToScan : packagesToScan) {
        // 省略其他部分代码...
        
        // 扫描给定的包名，其实也就是扫描 com.hmilyylimh.cloud.deploy 路径
        // 扫描那些属于 serviceAnnotationTypes 注解类型的 Bean 定义
        scanner.scan(packageToScan);
        // Finds all BeanDefinitionHolders of @Service whether @ComponentScan scans or not.
        Set<BeanDefinitionHolder> beanDefinitionHolders =
                findServiceBeanDefinitionHolders(scanner, packageToScan, registry, beanNameGenerator);
        if (!CollectionUtils.isEmpty(beanDefinitionHolders)) {
            // 省略其他部分代码...
            // 处理扫描到的 Bean 定义对象集合
            for (BeanDefinitionHolder beanDefinitionHolder : beanDefinitionHolders) {
                // 处理单个 Bean 定义对象
                processScannedBeanDefinition(beanDefinitionHolder, registry, scanner);
                servicePackagesHolder.addScannedClass(beanDefinitionHolder.getBeanDefinition().getBeanClassName());
            }
        } else {
            // 省略其他部分代码...
        }
        servicePackagesHolder.addScannedPackage(packageToScan);
    }
}
```

Dubbo 框架在服务注解这个后置处理器（ServiceAnnotationPostProcessor）中，利用扫描器，把含有 @DubboService 注解的类对应的 Bean 定义收集到了一块，然后逐个针对 Bean 定义进行了处理

```JAVA

// ServiceAnnotationPostProcessor#processScannedBeanDefinition
private void processScannedBeanDefinition(BeanDefinitionHolder beanDefinitionHolder, BeanDefinitionRegistry registry,
                                          DubboClassPathBeanDefinitionScanner scanner) {
    // 从 Bean 定义中找到对应的 Dubbo 接口服务类信息
    // 即：beanClass = com.hmilyylimh.cloud.deploy.demo.DemoFacadeImpl 类信息
    Class<?> beanClass = resolveClass(beanDefinitionHolder);
    // 从 beanClass 中找到含有 @DubboService 注解的对象
    // 准确来说，应该是查找 serviceAnnotationTypes 列表中有值的注解，取出找到的第一个
    Annotation service = findServiceAnnotation(beanClass);
    // 从刚刚找出的 service 注解对象中搜刮出注解属性值
    // @DubboService 中配置的 timeout = 8888 属性就会存在于 serviceAnnotationAttributes 变量中
    Map<String, Object> serviceAnnotationAttributes = AnnotationUtils.getAttributes(service, true);
    
    // 找到对应的服务接口名称
    // 即：serviceInterface = com.hmilyylimh.cloud.facade.demo.DemoFacade
    String serviceInterface = resolveInterfaceName(serviceAnnotationAttributes, beanClass);
    // annotatedServiceBeanName = demoFacadeImpl
    String annotatedServiceBeanName = beanDefinitionHolder.getBeanName();
    
    // 生成 ServiceBean 的 beanName
    String beanName = generateServiceBeanName(serviceAnnotationAttributes, serviceInterface);
    // 重新根据相关参数构建出一个新的 beanClass = ServiceBean.class 类型的 Bean 定义
    AbstractBeanDefinition serviceBeanDefinition =
            buildServiceBeanDefinition(serviceAnnotationAttributes, serviceInterface, annotatedServiceBeanName);
    // 然后将构建出来的 Bean 定义注册到 Spring 的容器中，等着后续的实例化操作
    registerServiceBeanDefinition(beanName, serviceBeanDefinition, serviceInterface);
}
```

3. 执行ServiceConfig.export 服务接口导出的方法
```JAVA

///////////////////////////////////////////////////
// ServiceConfig.export 服务接口导出的方法
///////////////////////////////////////////////////
public void export() {
    // 如果已导出的话，则不再处理导出逻辑
    if (this.exported) {
        return;
    }
    // 省略其他部分代码...
    // synchronized 保证线程安全，即只允许导出有且仅有一次
    synchronized (this) {
        // 再次检测，如果已导出的话，则不再处理导出逻辑
        if (this.exported) {
            return;
        }
        // Dubbo Config 属性重写
        if (!this.isRefreshed()) {
            this.refresh();
        }
        if (this.shouldExport()) {
            this.init();
            // 是否有设置延迟 delay 导出属性
            if (shouldDelay()) {
                doDelayExport();
            } else {
                // 导出的核心逻辑
                doExport();
            }
        }
    }
}
```

*总体流程如下*

![[Pasted image 20230207221531.png]]

#### 导出

```java

// 单个接口服务的导出方法，比如 DemoFacadeImpl 服务的导出，就会进入到这里来
org.apache.dubbo.config.ServiceConfig#doExport
                  ↓
// 因为存在多协议的缘故，所以这里就会将单个接口服务按照不同的协议进行导出
org.apache.dubbo.config.ServiceConfig#doExportUrls
                  ↓
// 将单个接口服务按照单个协议进行导出
// 其实是 doExportUrls 方法中循环调用了 doExportUrlsFor1Protocol 方法
org.apache.dubbo.config.ServiceConfig#doExportUrlsFor1Protocol
                  ↓
// 将单个接口服务按照单协议导出到多个注册中心上
org.apache.dubbo.config.ServiceConfig#exportUrl
// exportUrl 方法的实现体逻辑如下：
private void exportUrl(URL url, List<URL> registryURLs) {
    String scope = url.getParameter("scope");
    // don't export when none is configured
    if (!"none".equalsIgnoreCase(scope)) {
        // export to local if the config is not remote (export to remote only when config is remote)
        if (!"remote".equalsIgnoreCase(scope)) {
            // 本地导出
            exportLocal(url);
        }
        // export to remote if the config is not local (export to local only when config is local)
        if (!"local".equalsIgnoreCase(scope)) {
            // 远程导出
            url = exportRemote(url, registryURLs);
            if (!isGeneric(generic) && !getScopeModel().isInternal()) {
                MetadataUtils.publishServiceDefinition(url, providerModel.getServiceModel(), getApplicationModel());
            }
        }
    }
    this.urls.add(url);
}
```


##### 本地导出
一进入本地导出的方法，就将协议替换为了 injvm 协议，意思是，按照内置的 JVM 内存级别的协议也导出一下，最终调用了根据 url 进行服务导出的核心方法（doExportUrl）。

主要2个方法

###### 1. proxyFactory.getInvoker

使用了[[《Dubbo 源码剖析与实战 》学习笔记Day21]] 中的adapter 技术

doExportUrl 的入参 url 中确实没有 proxy 属性，那就有必要再看看 ProxyFactory 接口，默认设置的扩展点名称是什么：
```java
@SPI(value = "javassist", scope = FRAMEWORK)
public interface ProxyFactory { ... ｝
```

首先，先执行 ProxyFactory 接口的自适应扩展点代理类（ProxyFactory$Adaptive）的 getInvoker 方法。
然后，执行包装类（StubProxyFactoryWrapper）的 getInvoker 方法。
最后，执行 JavassistProxyFactory 实现类的 getInvoker 方法（这里调用时采用了[[《Dubbo 源码剖析与实战 》学习笔记Day19]]的技术）。

###### 2. protocolSPI.export

核心原理就是，将生成的 Invoker 代理类缓存到了 InjvmProtocol 中的 exporterMap 成员变量中。

```java

///////////////////////////////////////////////////
// org.apache.dubbo.rpc.protocol.injvm.InjvmProtocol#export
// InjvmProtocol 类中的 export 的导出核心逻辑，
// 其实就是将入参的 invoker 对象封装到 exporterMap 中而已
///////////////////////////////////////////////////
@Override
public <T> Exporter<T> export(Invoker<T> invoker) throws RpcException {
    return new InjvmExporter<T>(invoker, invoker.getUrl().getServiceKey(), exporterMap);
}
                  ↓
///////////////////////////////////////////////////                  
// org.apache.dubbo.rpc.protocol.injvm.InjvmExporter#InjvmExporter
// injvm 协议对应的导出对象
///////////////////////////////////////////////////
public class InjvmExporter<T> extends AbstractExporter<T> {
    private final String key;
    private final Map<String, Exporter<?>> exporterMap;
    InjvmExporter(Invoker<T> invoker, String key, Map<String, Exporter<?>> exporterMap) {
        super(invoker);
        this.key = key;
        this.exporterMap = exporterMap;
        // 存储到一个 exporterMap 集合中
        exporterMap.put(key, this);
    }
    // 省略其他部分逻辑...
}
```


##### 远程导出

```java

///////////////////////////////////////////////////
// org.apache.dubbo.config.ServiceConfig#exportRemote
// 远程导出的逻辑
///////////////////////////////////////////////////
private URL exportRemote(URL url, List<URL> registryURLs) {
    // 若注册中心地址集合不为空，则进行 for 循环处理
    if (CollectionUtils.isNotEmpty(registryURLs)) {
        // 开始循环每一个注册中心地址
        for (URL registryURL : registryURLs) {
            // service-discovery-registry 为了将服务的接口相关信息存储在内存中
            if ("service-discovery-registry".equals(registryURL.getProtocol())) {
                url = url.addParameterIfAbsent("service-name-mapping", "true");
            }
            //if protocol is only injvm ,not register
            // 如果发现注册中心地址是写着 injvm 协议的话，则跳过不做任何导出处理
            if ("injvm".equalsIgnoreCase(url.getProtocol())) {
                continue;
            }
            // dynamic = true 就会在注册中心创建临时节点
            // dynamic = false 就会在注册中心创建永久节点，若服务器宕机的话，需要人工手动删除注册中心上的提供方 IP 节点
            url = url.addParameterIfAbsent("dynamic", registryURL.getParameter("dynamic"));
            // 监控中心的地址，如果配置了的话，服务调用信息就会上报
            URL monitorUrl = ConfigValidationUtils.loadMonitor(this, registryURL);
            if (monitorUrl != null) {
                url = url.putAttribute("monitor", monitorUrl);
            }
            // For providers, this is used to enable custom proxy to generate invoker
            // 在提供方，这里支持自定义来生成代理
            String proxy = url.getParameter("proxy");
            if (StringUtils.isNotEmpty(proxy)) {
                registryURL = registryURL.addParameter("proxy", proxy);
            }
            // 有注册中心的逻辑：远程导出的核心逻辑
            // url：dubbo://192.168.100.183:28190/com.hmilyylimh.cloud.facade.demo.DemoFacade?anyhost=true&application=dubbo-19-dubbo-deploy-provider&background=false&bind.ip=192.168.100.183&bind.port=28190&deprecated=false&dubbo=2.0.2&dynamic=true&generic=false&interface=com.hmilyylimh.cloud.facade.demo.DemoFacade&methods=sayHello,say&pid=9636&qos.enable=false&register-mode=interface&release=3.0.7&side=provider&timeout=8888&timestamp=1670679510821
            // registryURL：registry://127.0.0.1:2181/org.apache.dubbo.registry.RegistryService?REGISTRY_CLUSTER=registryConfig&application=dubbo-19-dubbo-deploy-provider&dubbo=2.0.2&pid=9636&qos.enable=false&register-mode=interface&registry=zookeeper&release=3.0.7&timestamp=1670679510811
            doExportUrl(registryURL.putAttribute("export", url), true);
        }
    } else {
        // 省略其他部分逻辑...
        // 无注册中心的逻辑：远程导出的核心逻辑
        doExportUrl(url, true);
    }

    return url;
}
                  ↓
///////////////////////////////////////////////////                  
// org.apache.dubbo.config.ServiceConfig#doExportUrl
// 通用方法，根据给定的入参 url 进行服务导出
///////////////////////////////////////////////////
private void doExportUrl(URL url, boolean withMetaData) {
    // url 对应的内存值为：injvm://127.0.0.1/com.hmilyylimh.cloud.facade.demo.DemoFacade?anyhost=true&application=dubbo-19-dubbo-deploy-provider&background=false&bind.ip=192.168.100.183&bind.port=28190&deprecated=false&dubbo=2.0.2&dynamic=true&generic=false&interface=com.hmilyylimh.cloud.facade.demo.DemoFacade&methods=sayHello,say&pid=15092&qos.enable=false&register-mode=interface&release=3.0.7&side=provider&timeout=8888&timestamp=1670674553481
    // proxyFactory 为代理自适应扩展点
    // 获取经过 AbstractProxyInvoker 包装过的 Wrapper 动态代理类
    // 即 invoker 是 AbstractProxyInvoker 类型的，
    // 然后 AbstractProxyInvoker 中持有了 Wrapper 动态代理类
    Invoker<?> invoker = proxyFactory.getInvoker(ref, (Class) interfaceClass, url);
    if (withMetaData) {
        invoker = new DelegateProviderMetaDataInvoker(invoker, this);
    }
    // protocolSPI 为协议自定义扩展点
    // 将 invoker 按照指定的协议进行导出
    Exporter<?> exporter = protocolSPI.export(invoker);
    exporters.add(exporter);
}
```

三个逻辑

- 第一，是否有 registryURL 注册中心地址，会让导出的逻辑不太一样。有 registryURL，则用 registryURL 传入到 doExportUrl 方法，无 registryURL，则用接口服务的地址传入到 doExportUrl 方法。
- 第二，使用 registryURL 传入到 doExportUrl 方法，有个小细节，会将接口服务的地址内容以 key = export 属性形式，放在 registryURL 中。
- 第三，本地导出和远程导出，都调用同一个 doExportUrl 方法，也就意味着导出的主流程代码还是之前的两行代码，只不过远程导出时会走其他的实现类而已。

**_主要export方法_**

```java

///////////////////////////////////////////////////
// org.apache.dubbo.registry.integration.RegistryProtocol#export
// 远程导出核心逻辑，开启Netty端口服务 + 向注册中心写数据
///////////////////////////////////////////////////
@Override
public <T> Exporter<T> export(final Invoker<T> originInvoker) throws RpcException {
    // originInvoker.getUrl()：其实是注册中心地址
    // originInvoker.getUrl().toFullString()：registry://127.0.0.1:2181/org.apache.dubbo.registry.RegistryService?REGISTRY_CLUSTER=registryConfig&application=dubbo-19-dubbo-deploy-provider&dubbo=2.0.2&pid=13556&qos.enable=false&register-mode=interface&registry=zookeeper&release=3.0.7&timestamp=1670717595475
    // registryUrl：zookeeper://127.0.0.1:2181/org.apache.dubbo.registry.RegistryService?REGISTRY_CLUSTER=registryConfig&application=dubbo-19-dubbo-deploy-provider&dubbo=2.0.2&pid=13556&qos.enable=false&register-mode=interface&release=3.0.7&timestamp=1670717595475
    
    // 从 originInvoker 取出 "registry" 的属性值，结果取出了 zookeeper 值
    // 然后将 zookeeper 替换协议 "protocol" 属性的值就变成了 registryUrl
    URL registryUrl = getRegistryUrl(originInvoker);
    
    // providerUrl：dubbo://192.168.100.183:28190/com.hmilyylimh.cloud.facade.demo.DemoFacade?anyhost=true&application=dubbo-19-dubbo-deploy-provider&background=false&bind.ip=192.168.100.183&bind.port=28190&deprecated=false&dubbo=2.0.2&dynamic=true&generic=false&interface=com.hmilyylimh.cloud.facade.demo.DemoFacade&methods=sayHello,say&pid=13556&qos.enable=false&register-mode=interface&release=3.0.7&side=provider&timeout=8888&timestamp=1670717595488
    // 从 originInvoker.getUrl() 注册中心地址中取出 "export" 属性值
    URL providerUrl = getProviderUrl(originInvoker);
    // 省略部分其他代码...
    
    // 又看到了一个“本地导出”，此本地导出并不是之前看到的“本地导出”
    // 这里是注册中心协议实现类的本地导出，是需要本地开启20880端口的netty服务
    final ExporterChangeableWrapper<T> exporter = doLocalExport(originInvoker, providerUrl);
    
    // 根据 registryUrl 获取对应的注册器，这里获取的是对象从外层到内层依次是：
    // ListenerRegistryWrapper -> ZookeeperRegistry，最终拿到了 zookeeper 注册器
    final Registry registry = getRegistry(registryUrl);
    final URL registeredProviderUrl = getUrlToRegistry(providerUrl, registryUrl);
    boolean register = providerUrl.getParameter(REGISTER_KEY, true) && registryUrl.getParameter(REGISTER_KEY, true);
    if (register) {
        // 向 zookeeper 进行写数据，将 registeredProviderUrl 写到注册中心服务中去
        register(registry, registeredProviderUrl);
    }
    // 省略部分其他代码...
.    
}
```

- 首先，从传进来的 Invoker 代理对象中，取出注册注册中心地址，并且从注册中心地址中取出 registry 属性值得到 zookeeper 值，摇身一变，生成了一个以 zookeeper 为协议的新 registryUrl 地址。
- 然后，再次看到了一个 doLocalExport 方法，但是这个方法不是我们之前看到的“本地导出”，这里是注册协议实现类中本地导出，主要是开启本地 Dubbo 协议端口的 Netty 服务。
- 最后，从 registryUrl 中，根据 zookeeper 获取到 ZookeeperRegistry，并且，把构建好的提供方接口服务地址，写到 Zookeeper 注册中心服务去。

###### netty连接示意图

![[Pasted image 20230207231057.png]]

#### 注册

利用 Zookeeper 客户端，往 Zookeeper 服务端写了一条数据，即创建了一个文件目录而已，这就是服务注册的底层核心原理。

##### 主要流程

![[Pasted image 20230207231242.png]]


## 地址

此文章为2月day2 学习笔记，内容来源于极客时间《[Dubbo源码与实战]([[19｜发布流程：带你一窥服务发布的三个重要环节 (geekbang.org)](https://time.geekbang.org/column/article/620988))》，推荐该课程


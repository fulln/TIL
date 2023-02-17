
##  协议扩展：如何快速控制应用的上下线？

dubbo admin控制台服务过多导致管理混乱，短时间内的dubbo-admin内存数据急剧变化。需要改造

### dubbo-admin 去掉控制台

从控制台下线的源码入手
```java

public void disableProvider(Long id) {
  // 省略了其他代码
  Provider oldProvider = findProvider(id);
  if (oldProvider == null) {
    throw new IllegalStateException("Provider was changed!");
  }

  if (oldProvider.isDynamic()) {
    // 保证disable的override唯一
    if (oldProvider.isEnabled()) {
      Override override = new Override();
      override.setAddress(oldProvider.getAddress());
      override.setService(oldProvider.getService());
      override.setEnabled(true);
      override.setParams("disabled" + "=true");
      overrideService.saveOverride(override);
      return;
    }
    // 省略了其他代码
  } else {
    oldProvider.setEnabled(false);
    updateProvider(oldProvider);
  }
}
```

可以通过url 直接控制服务的下线，只需要下线的时候直接把这串信息写到注册中心去就行了。

### 协议扩展控制上线

![[Pasted image 20230217223358.png]]


- 进行协议拦截，主要以禁用协议的方式进行接口注册。
- 在拦截协议的同时，把原始注册信息 URL 保存到磁盘文件中。
- 待服务重新部署成功后，利用自制的简单页面进行简单操作，发布上线指令操作。
- 发布上线的指令的背后操作，就是把对应应用机器上磁盘文件中的原始注册信息 URL 取出来。
- 最后利用操作注册中心的工具类，把取出来的原始注册信息 URL 全部写到注册中心。

```java

///////////////////////////////////////////////////
// 禁用协议包装器
///////////////////////////////////////////////////
public class OverrideProtocolWrapper implements Protocol {
    private final Protocol protocol;
    private Registry registry;
    // 存储原始注册信息的，模拟存储硬盘操作
    private static final List<URL> UN_REGISTRY_URL_LIST = new ArrayList<>();
    // 包装器的构造方法写法
    public OverrideProtocolWrapper(Protocol protocol) {
        this.protocol = protocol;
    }
    
    @Override
    public <T> Exporter<T> export(Invoker<T> invoker) throws RpcException {
        // 如果是注册协议的话，那么就先注册一个 override 到 zk 上，表示禁用接口被调用
        if (UrlUtils.isRegistry(invoker.getUrl())) {
            if (registry == null) {
                registry = getRegistry(invoker);
            }
            // 注册 override url，主要是在这一步让提供方无法被提供方调用
            doRegistryOverrideUrl(invoker);
        }
        
        // 接下来原来该怎么调用还是接着怎么进行下一步调用
        return this.protocol.export(invoker);
    }
    
    private <T> void doRegistryOverrideUrl(Invoker<T> invoker) {
        // 获取原始接口注册信息
        URL originalProviderUrl = getProviderUrl(invoker);
        // 顺便将接口注册的原始信息保存到内存中，模拟存储磁盘的过程
        UN_REGISTRY_URL_LIST.add(originalProviderUrl);
        
        // 构建禁用协议对象
        OverrideBean override = new OverrideBean();
        override.setAddress(originalProviderUrl.getAddress());
        override.setService(originalProviderUrl.getServiceKey());
        override.setEnabled(true);
        override.setParams("disabled=true");
        
        // 将禁用协议写到注册中心去
        registry.register(override.toUrl());
    }
    // 获取操作 Zookeeper 的注册器
    private Registry getRegistry(Invoker<?> originInvoker) {
        URL registryUrl = originInvoker.getUrl();
        if (REGISTRY_PROTOCOL.equals(registryUrl.getProtocol())) {
            String protocol = registryUrl.getParameter(REGISTRY_KEY, DEFAULT_REGISTRY);
            registryUrl = registryUrl.setProtocol(protocol).removeParameter(REGISTRY_KEY);
        }
        RegistryFactory registryFactory = ScopeModelUtil.getExtensionLoader
                (RegistryFactory.class, registryUrl.getScopeModel()).getAdaptiveExtension();
        return registryFactory.getRegistry(registryUrl);
    }
    // 获取原始注册信息URL对象
    private URL getProviderUrl(final Invoker<?> originInvoker) {
        return (URL) originInvoker.getUrl().getAttribute("export");
    }
    @Override
    public <T> Invoker<T> refer(Class<T> type, URL url) throws RpcException {
        return protocol.refer(type, url);
    }
    @Override
    public int getDefaultPort() {
        return protocol.getDefaultPort();
    }
    @Override
    public void destroy() {
        protocol.destroy();
    }
}

///////////////////////////////////////////////////
// 提供方资源目录文件
// 路径为：/META-INF/dubbo/org.apache.dubbo.rpc.Protocol
///////////////////////////////////////////////////
com.hmilyylimh.cloud.protocol.config.ext.OverrideProtocolWrapper

///////////////////////////////////////////////////
// 资源目录文件
// 路径为：/dubbo.properties
// 只进行接口级别注册
///////////////////////////////////////////////////
dubbo.application.register-mode=interface
```


### 使用场景

第一，收集接口发布列表，当我们需要统计系统的接口是否都已经发布时，可以通过协议扩展的方式来统计处理。
第二，禁用接口注册，根据一些黑白名单，在应用层面控制哪些接口需要注册，哪些接口不需要注册。
第三，多协议扩展，比如当市场上冒出一种新的协议，你也想在 Dubbo 框架这边支持，可以考虑像 DubboProtocol、HttpProtocol 这些类一样，扩展新的协议实现类。


## 地址

此文章为2月day11 学习笔记，内容来源于极客时间《[27｜协议扩展：如何快速控制应用的上下线？ (geekbang.org)](https://time.geekbang.org/column/article/625403)》，

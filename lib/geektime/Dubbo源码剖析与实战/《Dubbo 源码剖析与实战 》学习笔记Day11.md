#极客时间 #dubbo 

##  课程内容

### dubbo 日志检索

> 市面上常用的是使用动态链路追踪框架,如`skywalking` ,`pinpoint` 等常用框架

1. 一次请求动态生成序列号,传递要需要的系统中
	- 显示传递  => 在请求参数中,添加序列号字段.按照一定规约来进行传递,但是有改造大,局限性大等问题
	- 隐式传递  => 把业务对象划分到业务属性，把请求序列号划分到技术属性,在技术属性中传递需要的参数

#### dubbo参数传递

![[Pasted image 20230126143129.png]]

从上面的图中,可以看出,在调用过程中,我们定义2个dubbo的过滤器, 就可以将参数传递到RpcContext中.

```java

@Activate(group = PROVIDER, order = -9000)
public class ReqNoProviderFilter implements Filter {
    public static final String TRACE_ID = "TRACE-ID";
    @Override
    public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {
        // 获取入参的跟踪序列号值
        Map<String, Object> attachments = invocation.getObjectAttachments();
        String reqTraceId = attachments != null ? (String) attachments.get(TRACE_ID) : null;
        
        // 若 reqTraceId 为空则重新生成一个序列号值，序列号在一段相对长的时间内唯一足够了
        reqTraceId = reqTraceId == null ? generateTraceId() : reqTraceId;
        
        // 将序列号值设置到上下文对象中
        RpcContext.getServerAttachment().setObjectAttachment(TRACE_ID, reqTraceId);
        
        // 并且将序列号设置到日志打印器中，方便在日志中体现出来
        MDC.put(TRACE_ID, reqTraceId);
        
        // 继续后面过滤器的调用
        return invoker.invoke(invocation);
    }
}

@Activate(group = CONSUMER, order = Integer.MIN_VALUE + 1000)
public class ReqNoConsumerFilter implements Filter, Filter.Listener {
    public static final String TRACE_ID = "TRACE-ID";
    @Override
    public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {
        // 从上下文对象中取出跟踪序列号值
        String existsTraceId = RpcContext.getServerAttachment().getAttachment(TRACE_ID);
        
        // 然后将序列号值设置到请求对象中
        invocation.getObjectAttachments().put(TRACE_ID, existsTraceId);
        RpcContext.getClientAttachment().setObjectAttachment(TRACE_ID, existsTraceId);
        
        // 继续后面过滤器的调用
        return invoker.invoke(invocation);
    }
}
```

#### 应用

1. 传递请求流水号，分布式应用中通过链路追踪号来全局检索日志。
2. 传递用户信息，以便不同系统在处理业务逻辑时可以获取用户层面的一些信息。
3. 传递凭证信息，以便不同系统可以有选择性地取出一些数据做业务逻辑，比如 Cookie、Token 等。

#### RpcContext 的4种属性对应的生命周期

1. SERVER_LOCAL --> provider侧使用,`org.apache.dubbo.rpc.RpcContext.RestoreContext#restore`中被设置,在 Provider 转为 Consumer 角色时被清除数据。
2. CLIENT_ATTACHMENT --> 将附属信息作为 Consumer 传递到下一跳 Provider，在consumer和provide的Filter中的`onResponse/onerror`被清除.
3. SERVER_ATTACHMENT --> 作为 Provider 侧用于接收上一跳 Consumer 的发来附属信息，在consumer和provide的Filter中的`onResponse/onerror`被清除.
4. SERVICE_CONTEXT --> 将附属信息作为 Provider 返回给 Consumer ,在provide的Filter中的`onResponse/onerror`被清除.

### dubbo 泛化调用

主要是针对透传性质的服务开发, 提高其效率

#### 使用手段

- 反射
	通过编写commonInvoke方法, 将入参序列化,调用时通过反射去发起RPC调用,但是无法精简url地址,下游接口字段等参数

- 泛化调用
要实现泛化调用,需要知道如何寻找对应dubbobean对象去调用,这里可以参考下`@Reference`

##### @DubboReference  实现方式

![[Pasted image 20230126151445.png]]


##### commonInvoke 改造

```java

@RestController
public class CommonController {
    // 响应码为成功时的值
    public static final String SUCC = "000000";
    
    // 定义URL地址
    @PostMapping("/gateway/{className}/{mtdName}/{parameterTypeName}/request")
    public String commonRequest(@PathVariable String className,
                                @PathVariable String mtdName,
                                @PathVariable String parameterTypeName,
                                @RequestBody String reqBody){
        // 将入参的req转为下游方法的入参对象，并发起远程调用
        return commonInvoke(className, parameterTypeName, mtdName, reqBody);
    }
    
    /**
     * <h2>模拟公共的远程调用方法.</h2>
     *
     * @param className：下游的接口归属方法的全类名。
     * @param mtdName：下游接口的方法名。
     * @param parameterTypeName：下游接口的方法入参的全类名。
     * @param reqParamsStr：需要请求到下游的数据。
     * @return 直接返回下游的整个对象。
     * @throws InvocationTargetException
     * @throws IllegalAccessException
     */
    public static String commonInvoke(String className,
                                      String mtdName,
                                      String parameterTypeName,
                                      String reqParamsStr) {
        // 然后试图通过类信息对象想办法获取到该类对应的实例对象
        ReferenceConfig<GenericService> referenceConfig = createReferenceConfig(className);
        
        // 远程调用
        GenericService genericService = referenceConfig.get();
        Object resp = genericService.$invoke(
                mtdName,
                new String[]{parameterTypeName},
                new Object[]{JSON.parseObject(reqParamsStr, Map.class)});
        
        // 判断响应对象的响应码，不是成功的话，则组装失败响应
        if(!SUCC.equals(OgnlUtils.getValue(resp, "respCode"))){
            return RespUtils.fail(resp);
        }
        
        // 如果响应码为成功的话，则组装成功响应
        return RespUtils.ok(resp);
    }
    
    private static ReferenceConfig<GenericService> createReferenceConfig(String className) {
        DubboBootstrap dubboBootstrap = DubboBootstrap.getInstance();
        
        // 设置应用服务名称
        ApplicationConfig applicationConfig = new ApplicationConfig();
        applicationConfig.setName(dubboBootstrap.getApplicationModel().getApplicationName());
        
        // 设置注册中心的地址
        String address = dubboBootstrap.getConfigManager().getRegistries().iterator().next().getAddress();
        RegistryConfig registryConfig = new RegistryConfig(address);
        ReferenceConfig<GenericService> referenceConfig = new ReferenceConfig<>();
        referenceConfig.setApplication(applicationConfig);
        referenceConfig.setRegistry(registryConfig);
        referenceConfig.setInterface(className);
        
        // 设置泛化调用形式
        referenceConfig.setGeneric("true");
        // 设置默认超时时间5秒
        referenceConfig.setTimeout(5 * 1000);
        return referenceConfig;
    }
}
```
	
##### 接口代理对象的核心逻辑

1. URL 地址增加了一个方法参数类名的维度，意味着通过类名、方法名、方法参数类名可以访问后台的提供者；
2. 通过接口类名来创建 **ReferenceConfig** 对象，并设置 generic = true 的核心属性；
3. 通过 referenceConfig.get 方法得到 **genericService** 泛化对象；
4. 将方法名、方法参数类名、业务请求参数传入泛化对象的 $invoke 方法中进行远程 Dubbo 调用，并返回响应对象；
5. 通过 Ognl 表达式语言从响应对象取出 respCode 响应码判断并做最终返回。

#### 泛化调用的运用

1. 第一，透传式调用，发起方只是想调用提供者拿到结果，没有过多的业务逻辑诉求，即使有，也是拿到结果后再继续做分发处理。
2. 第二，代理服务，所有的请求都会经过代理服务器，而代理服务器不会感知任何业务逻辑，只是一个通道，接收数据 -> 发起调用 -> 返回结果，调用流程非常简单纯粹。
3. 第三，前端网关，有些内网环境的运营页面，对 URL 的格式没有那么严格的讲究，页面的功能都是和后端服务一对一的操作，非常简单直接。


## 课程地址

[03｜隐式传递：如何精准找出一次请求的全部日志？](https://time.geekbang.org/column/article/613301)
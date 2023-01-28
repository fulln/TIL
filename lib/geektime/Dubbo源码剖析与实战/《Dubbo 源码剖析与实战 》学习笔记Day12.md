#java #dubbo #极客时间 

## 课程内容

### dubbo 调用

#### 动态调用代码

1. telnet 调用
2. 使用`ReferenceConfig` 类中拼装对应IP,port,url等参数,然后调用`get`

##### url拼装规则

调用了URLStrParser 类来解析为可以被识别的 URL 对象
url 的构成规则为：`[protocol://][username:password@][host:port]/[path][?k1=v1&k2=v2]`


通过上面第二点,我们可以设置动态的dubbo调用入口

- 首先，定义一个 MonsterController 控制器专门来接收页面的请求。
- 其次，创建泛化调用所需的 referenceConfig 对象，并将 url 设置到 referenceConfig 对象中。
- 最后，套用之前学过的泛化调用代码，完成页面数据的转发。

#### 修复万能逻辑Dubbo接口

```java

public interface MonsterFacade {
    // 定义了一个专门处理万能修复逻辑的Dubbo接口
    AbstractResponse heretical(HereticalReq req);
}

public class MonsterFacadeImpl implements MonsterFacade {
    @Override
    AbstractResponse heretical(HereticalReq req){
        // 编译 Java 代码，然后变成 JVM 可识别的 Class 对象信息
        Class<?> javaClass = compile(req.getJavaCode());
        
        // 为 Class 对象信息，自定义一个名称，将来创建 Spring 单例对象要用到
        String beanName = "Custom" + javaClass.getSimpleName();
        
        // 通过 Spring 来创建单例对象
        generateSpringBean(beanName, javaClass);
        
        // 获取 beanName 对应的单例对象
        MonsterInvokeRunnable runnable = (MonsterAction)SpringContextUtils.getBean(beanName);
        
        // 执行单例对象的方法即可
        Object resp = runnable.run(req.getReqParamsMap());
        
        // 返回结果
        return new AbstractResponse(resp);
    }
    
    // 利用 groovy-all.jar 中的 groovyClassLoader 来编译 Java 代码
    private Class<?> compile(String javaCode){
        return groovyClassLoader.parseClass(javaCode);
    }
    
    // 生成Spring容器Bean对象
    private void generateSpringBean(String beanName, Class<?> javaClass){
        // 构建 Bean 定义对象
        BeanDefinitionBuilder beanDefinitionBuilder =
                BeanDefinitionBuilder.genericBeanDefinition(javaClass);
        AbstractBeanDefinition rawBeanDefinition = beanDefinitionBuilder.getRawBeanDefinition();
        
        // 将 bean 移交给 Spring 去管理
        ConfigurableApplicationContext appCtx =
                (ConfigurableApplicationContext)SpringContextUtils.getContext();
        appCtx.getAutowireCapableBeanFactory()
                .applyBeanPostProcessorsAfterInitialization(rawBeanDefinition, beanName);
        ((BeanDefinitionRegistry)appCtx.getBeanFactory()).registerBeanDefinition(beanName, rawBeanDefinition);
    }
}

```

上面的代码使用了Groovy 插件`groovy-all.jar` ,将接收的代码编译为class对象, 并执行达到修复任意代码的目的.

##### 使用场景

第一，修复产线事件，通过直连 + 泛化 + 动态代码编译执行，可以轻松临时解决产线棘手的问题。第二，绕过注册中心直接联调测试，有些公司由于测试环境的复杂性，有时候不得不采用简单的直连方式，来快速联调测试验证功能。
第三，检查服务存活状态，如果需要针对多台机器进行存活检查，那就需要循环调用所有服务的存活检查接口。


### dubbo事件通知

#### 代码解耦合

1. 功能相关性。将一些功能非常相近的汇聚成一块
2. 密切相关性。按照与主流程的密切相关性，将一个个小功能分为密切与非密切。
3. 状态变更性。按照是否有明显业务状态的先后变更，将一个个小功能再归类。

#### 代码串联
事件驱动

- aop拦截

##### dubbo的拦截实现

```java

@Activate(group = CommonConstants.CONSUMER)
public class FutureFilter implements ClusterFilter, ClusterFilter.Listener {
    protected static final Logger logger = LoggerFactory.getLogger(FutureFilter.class);
    @Override
    public Result invoke(final Invoker<?> invoker, final Invocation invocation) throws RpcException {
        // 调用服务之前：执行Dubbo接口配置中指定服务中的onInvoke方法
        fireInvokeCallback(invoker, invocation);
        // need to configure if there's return value before the invocation in order to help invoker to judge if it's
        // necessary to return future.
        // 调用服务并返回调用结果
        return invoker.invoke(invocation);
    }
    
    // 调用服务之后：
    // 正常返回执行Dubbo接口配置中指定服务中的onReturn方法
    // 异常返回执行Dubbo接口配置中指定服务中的onThrow方法
    @Override
    public void onResponse(Result result, Invoker<?> invoker, Invocation invocation) {
        if (result.hasException()) {
            // 调用出现了异常之后的应对处理
            fireThrowCallback(invoker, invocation, result.getException());
        } else {
            // 正常调用返回结果的应对处理
            fireReturnCallback(invoker, invocation, result.getValue());
        }
    }
    
    // 调用框架异常后：
    // 异常返回执行Dubbo接口配置中指定服务中的onThrow方法
    @Override
    public void onError(Throwable t, Invoker<?> invoker, Invocation invocation) {
        fireThrowCallback(invoker, invocation, t);
    }
}    
```

可以看出,利用`FutureFilter`过滤器,做到了
1. 在 invoker.invoke(invocation) 方法之前，利用 fireInvokeCallback 方法反射调用了接口配置中指定服务中的 onInvoke 方法。
2. 在 onResponse 响应时，处理了正常返回和异常返回的逻辑，分别调用了接口配置中指定服务中的 onReturn、onThrow 方法。
3. 最后在 onError 框架异常后，调用了接口配置中指定服务中的 onThrow 方法。

##### dubbo 拦截使用方式

```java

@DubboService
@Component
public class PayFacadeImpl implements PayFacade {
    @Autowired
    @DubboReference(
            /** 为 DemoRemoteFacade 的 sayHello 方法设置事件通知机制 **/
            methods = {@Method(
                    name = "sayHello",
                    oninvoke = "eventNotifyService.onInvoke",
                    onreturn = "eventNotifyService.onReturn",
                    onthrow = "eventNotifyService.onThrow")}
    )
    private DemoRemoteFacade demoRemoteFacade;
    
    // 商品支付功能：一个大方法
    @Override
    public PayResp recvPay(PayReq req){
        // 支付核心业务逻辑处理
        method1();
        // 返回支付结果
        return buildSuccResp();
    }
    private void method1() {
        // 省略其他一些支付核心业务逻辑处理代码
        demoRemoteFacade.sayHello(buildSayHelloReq());
    }
}

// 专门为 demoRemoteFacade.sayHello 该Dubbo接口准备的事件通知处理类
@Component("eventNotifyService")
public class EventNotifyServiceImpl implements EventNotifyService {
    // 调用之前
    @Override
    public void onInvoke(String name) {
        System.out.println("[事件通知][调用之前] onInvoke 执行.");
    }
    // 调用之后
    @Override
    public void onReturn(String result, String name) {
        System.out.println("[事件通知][调用之后] onReturn 执行.");
        // 埋点已支付的商品信息
        method2();
        // 发送支付成功短信给用户
        method3();
        // 通知物流派件
        method4();
    }
    // 调用异常
    @Override
    public void onThrow(Throwable ex, String name) {
        System.out.println("[事件通知][调用异常] onThrow 执行.");
    }
}


```

#### 运用场景

- 第一，职责分离，可以按照功能相关性剥离开，让各自的逻辑是内聚的、职责分明的。
- 第二，解耦，把复杂的面向过程风格的一坨代码分离，可以按照功能是技术属性还是业务属性剥离。
- 第三，事件溯源，针对一些事件的实现逻辑，如果遇到未知异常后还想再继续尝试重新执行的话，可以考虑事件持久化并支持在一定时间内重新回放执行。

## 课程地址

[05｜点点直连：点对点搭建产线“后门”的万能管控](https://time.geekbang.org/column/article/613319)

[06｜事件通知：一招打败各种神乎其神的回调事件](https://time.geekbang.org/column/article/613332)
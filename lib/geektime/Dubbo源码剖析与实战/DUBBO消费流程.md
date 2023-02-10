#java #极客时间 #dubbo 

## 内容

### 消费方的调用流程
>不看过程，只看结论；再看细节，再看过程。

会添加@DubboReference 进行远程调用

#### 远程调用

##### JDK代理

代码会生成对应$Proxy 类名、代理类中的 h 成员变量属于 JdkDynamicAopProxy 类型，综合判断，这是采用 JDK 代理动态

代理类中2个主要的成员字段

1. targetSource

变量类为： ReferenceBean$DubboReferenceLazyInitTargetSource，最终还是调用的 ReferenceConfig 的 get 方法。进入到[dubbo订阅流程](./DUBBO订阅流程)

2. interfaces

除了有我们调用下游的接口 DemoFacade，还有一个回声测试接口（EchoService）和一个销毁引用的接口（Destroyable）

这2个接口就是在创建JDK代理的时候一并传入的。这样一个代理对象就有了多种效果


#####  InvokerInvocationHandler

实现了JDK的 InvokerInvocationHandler 接口，是dubbo框架中接受代理触发的入口

```java

///////////////////////////////////////////////////                  
// org.apache.dubbo.rpc.proxy.InvokerInvocationHandler#invoke
// JDK 代理被触发调用后紧接着就开始进入 Dubbo 框架的调用，
// 因此跟踪消费方调用的入口，一般直接搜索这个 InvokerInvocationHandler 即可，
// 再说一点，这个 InvokerInvocationHandler 继承了 InvocationHandler 接口。
///////////////////////////////////////////////////
@Override
public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
    // 如果方法所在的类是 Object 类型的话，则不做任何处理
    // 毕竟 Object 类型是 JDK 源码中的类，也不是 Dubbo 框架处理的重点
    if (method.getDeclaringClass() == Object.class) {
        return method.invoke(invoker, args);
    }
    
    // 获取方法名，方法参数类型
    String methodName = method.getName();
    Class<?>[] parameterTypes = method.getParameterTypes();
    // 如果参数类型个数是 0 个的话，则表示是无参数方法
    // 既然是无参数方法的话，对于一些特殊的方法需要尽可能的在入口处解决
    // 因此对于 Object 中的 toString、hashCode 方法，Destroyable 接口实现类的 $destroy 方法
    if (parameterTypes.length == 0) {
        if ("toString".equals(methodName)) {
            return invoker.toString();
        } else if ("$destroy".equals(methodName)) {
            invoker.destroy();
            return null;
        } else if ("hashCode".equals(methodName)) {
            return invoker.hashCode();
        }
    } 
    // 如果方法参数个数为 1 个，并且还是 equals 方法，则也不是 Dubbo 框架处理的重点
    else if (parameterTypes.length == 1 && "equals".equals(methodName)) {
        return invoker.equals(args[0]);
    }
    
    // 还能来到这里，说明这才是 Dubbo 框架需要介入处理的方法
    // 前面那么多提前返回的逻辑，在前几次阅读时，根本不需要细看，可以直接跳过不看
    RpcInvocation rpcInvocation = new RpcInvocation(serviceModel, method, invoker.getInterface().getName(), protocolServiceKey, args);
    if (serviceModel instanceof ConsumerModel) {
        rpcInvocation.put(Constants.CONSUMER_MODEL, serviceModel);
        rpcInvocation.put(Constants.METHOD_MODEL, ((ConsumerModel) serviceModel).getMethodModel(method));
    }
    // 然后转手就把逻辑全部收口到一个 InvocationUtil 类中，
    // 从命名也看得出，就是一个调用的工具类
    return InvocationUtil.invoke(invoker, rpcInvocation);
}
```

从上往下大致浏览一遍。
1. 从代码表面的流程看，一些 toString、$destroy、hashCode 等方法做了特殊的逻辑提前返回了，最终调用 InvocationUtil 的 invoke 方法进行了收口处理。
2. 从方法的入参和返回值看，有方法对象、入参数据、代理对象，满足了反射调用的基本要素，调用后返回的数据，自然就是我们需要的结果。
3. 再看方法实现体的一些细节，发现最终并没有使用 proxy 代理对象，而是使用了 invoker + rpcInvocation 传入 InvocationUtil 工具类，完成了逻辑收口。

##### MigrationInvoker

```java

///////////////////////////////////////////////////                  
// org.apache.dubbo.registry.client.migration.MigrationInvoker#invoke
// 迁移兼容调用器
///////////////////////////////////////////////////
@Override
public Result invoke(Invocation invocation) throws RpcException {
    if (currentAvailableInvoker != null) {
        if (step == APPLICATION_FIRST) {
            // call ratio calculation based on random value
            if (promotion < 100 && ThreadLocalRandom.current().nextDouble(100) > promotion) {
                return invoker.invoke(invocation);
            }
        }
        return currentAvailableInvoker.invoke(invocation);
    }

    switch (step) {
        case APPLICATION_FIRST:
            if (checkInvokerAvailable(serviceDiscoveryInvoker)) {
                currentAvailableInvoker = serviceDiscoveryInvoker;
            } else if (checkInvokerAvailable(invoker)) {
                currentAvailableInvoker = invoker;
            } else {
                currentAvailableInvoker = serviceDiscoveryInvoker;
            }
            break;
        case FORCE_APPLICATION:
            currentAvailableInvoker = serviceDiscoveryInvoker;
            break;
        case FORCE_INTERFACE:
        default:
            currentAvailableInvoker = invoker;
    }

    return currentAvailableInvoker.invoke(invocation);
}
```

1. 主要是针对step的分发
2. 入参是invocation 是一个含有所有请求的接口，出参也是个包装类
3. 根据step进行新老订阅方案的兼容。

##### MockClusterInvoker

```java

///////////////////////////////////////////////////                  
// org.apache.dubbo.rpc.cluster.support.wrapper.MockClusterInvoker#invoke
// 调用异常时进行使用mock逻辑来处理数据的返回
///////////////////////////////////////////////////
@Override
public Result invoke(Invocation invocation) throws RpcException {
    Result result;
    // 从远程引用的url中看看有没有 mock 属性
    String value = getUrl().getMethodParameter(invocation.getMethodName(), "mock", Boolean.FALSE.toString()).trim();
    // mock 属性值为空的话，相当于没有 mock 逻辑，则直接继续后续逻辑调用
    if (ConfigUtils.isEmpty(value)) {
        //no mock
        result = this.invoker.invoke(invocation);
    } 
    // 如果 mock 属性值是以 force 开头的话
    else if (value.startsWith("force")) {
        // 那么就直接执行 mock 调用逻辑，
        // 用事先准备好的模拟逻辑或者模拟数据返回
        //force:direct mock
        result = doMockInvoke(invocation, null);
    } 
    // 还能来到这说明只是想在调用失败的时候尝试一下 mock 逻辑
    else {
        //fail-mock
        try {
            // 先正常执行业务逻辑调用
            result = this.invoker.invoke(invocation);
            //fix:#4585
            // 当业务逻辑执行有异常时，并且这个异常类属于RpcException或RpcException子类时，
            // 还有异常的原因如果是 Dubbo 框架层面的业务异常时，则不做任何处理。
            // 如果不是业务异常的话，则会继续尝试执行 mock 业务逻辑
            if(result.getException() != null && result.getException() instanceof RpcException){
                RpcException rpcException= (RpcException)result.getException();
                // 如果异常是 Dubbo 系统层面所认为的业务异常时，就不错任何处理
                if(rpcException.isBiz()){
                    throw  rpcException;
                }else {
                    // 能来到这里说明是不是业务异常的话，那就执行模拟逻辑
                    result = doMockInvoke(invocation, rpcException);
                }
            }
        } catch (RpcException e) {
            // 业务异常直接往上拋
            if (e.isBiz()) {
                throw e;
            }
            // 不是 Dubbo 层面所和认为的异常信息时代，
            // 直接
            result = doMockInvoke(invocation, e);
        }
    }
    return result;
}
```

#### 过滤器链

Cluster 这个关键字，想必你也想到了它是一个 SPI 接口，那在“发布流程”中我们也学过，远程导出和远程引用的时候，会用过滤器链把 invoker 层层包装起来,进入 FutureFilter、MonitorFilter 等过滤器

##### FailoverClusterInvoker

```java

///////////////////////////////////////////////////                  
// org.apache.dubbo.rpc.cluster.support.FailoverClusterInvoker#doInvoke
// 故障转移策略的核心逻辑实现类
///////////////////////////////////////////////////
@Override
@SuppressWarnings({"unchecked", "rawtypes"})
public Result doInvoke(Invocation invocation, final List<Invoker<T>> invokers, LoadBalance loadbalance) throws RpcException {
    List<Invoker<T>> copyInvokers = invokers;
    checkInvokers(copyInvokers, invocation);
    // 获取此次调用的方法名
    String methodName = RpcUtils.getMethodName(invocation);
    // 通过方法名计算获取重试次数
    int len = calculateInvokeTimes(methodName);
    // retry loop.
    // 循环计算得到的 len 次数
    RpcException le = null; // last exception.
    List<Invoker<T>> invoked = new ArrayList<Invoker<T>>(copyInvokers.size()); // invoked invokers.
    Set<String> providers = new HashSet<String>(len);
    for (int i = 0; i < len; i++) {
        //Reselect before retry to avoid a change of candidate `invokers`.
        //NOTE: if `invokers` changed, then `invoked` also lose accuracy.
        // 从第2次循环开始，会有一段特殊的逻辑处理
        if (i > 0) {
            // 检测 invoker 是否被销毁了
            checkWhetherDestroyed();
            // 重新拿到调用接口的所有提供者列表集合，
            // 粗俗理解，就是提供该接口服务的每个提供方节点就是一个 invoker 对象
            copyInvokers = list(invocation);
            // check again
            // 再次检查所有拿到的 invokes 的一些可用状态
            checkInvokers(copyInvokers, invocation);
        }
        // 选择其中一个，即采用了负载均衡策略从众多 invokers 集合中挑选出一个合适可用的
        Invoker<T> invoker = select(loadbalance, invocation, copyInvokers, invoked);
        invoked.add(invoker);
        // 设置 RpcContext 上下文
        RpcContext.getServiceContext().setInvokers((List) invoked);
        boolean success = false;
        try {
            // 得到最终的 invoker 后也就明确了需要调用哪个提供方节点了
            // 反正继续走后续调用流程就是了
            Result result = invokeWithContext(invoker, invocation);
            // 如果没有抛出异常的话，则认为正常拿到的返回数据
            // 那么设置调用成功标识，然后直接返回 result 结果
            success = true;
            return result;
        } catch (RpcException e) {
            // 如果是 Dubbo 框架层面认为的业务异常，那么就直接抛出异常
            if (e.isBiz()) { // biz exception.
                throw e;
            }
            // 其他异常的话，则不继续抛出异常，那么就意味着还可以有机会再次循环调用
            le = e;
        } catch (Throwable e) {
            le = new RpcException(e.getMessage(), e);
        } finally {
            // 如果没有正常返回拿到结果的话，那么把调用异常的提供方地址信息记录起来
            if (!success) {
                providers.add(invoker.getUrl().getAddress());
            }
        }
    }
    
    // 如果 len 次循环仍然还没有正常拿到调用结果的话，
    // 那么也不再继续尝试调用了，直接索性把一些需要开发人员关注的一些信息写到异常描述信息中，通过异常方式拋出去
    throw new RpcException(le.getCode(), "Failed to invoke the method "
            + methodName + " in the service " + getInterface().getName()
            + ". Tried " + len + " times of the providers " + providers
            + " (" + providers.size() + "/" + copyInvokers.size()
            + ") from the registry " + directory.getUrl().getAddress()
            + " on the consumer " + NetUtils.getLocalHost() + " using the dubbo version "
            + Version.getVersion() + ". Last error is: "
            + le.getMessage(), le.getCause() != null ? le.getCause() : le);
}
```

1. for循环，根据方法名，重试等参数进行select操作，然后拿到合适的invoke
2. 从方法的入参和返回值看，入参是 invocation、invokers、loadbalance 三个参数，猜测应该就是利用 loadbalance 负载均衡器，从 invokers 集合中，选择一个 invoker 来发送 invocation 数据，发送完成后得到了返参的 Result 结果。
3. 通过计算 retries 属性值得到重试次数并循环，每次循环都是利用负载均衡器选择一个进行调用，如果出现非业务异常，继续循环调用，直到所有次数循环完，还是没能拿到结果的话就会抛出 RpcException 异常了。


## 地址

此文章为2月day5 学习笔记，内容来源于极客时间《[21｜调用流程：消费方的调用流程体系，你知道多少？ (geekbang.org)](https://time.geekbang.org/column/article/621733)》，推荐该课程

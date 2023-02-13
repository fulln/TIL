#java #dubbo #极客时间 

## 集群扩展：发送请求遇到服务不可用，怎么办？

### 链路异常处理

1. 超时异常

直接从异常端发现Caused by 引发的 TimeoutException 异常类。属于常规异常，

但如果提供方根本没有收到消费方的任何请求，则
 - 从监控平台看目标是否继续接收流量
 - 从 Prometheus 上观察消费方到目标 IP 的 TCP 连接状况
 - 从网络层面通过 tcpdump 抓包检测消费方到目标 IP 的连通性等等

2. 无提供者异常

No provider available 这样的关键字，对应源码位置为：

```java
protected void checkInvokers(List<Invoker<T>> invokers, Invocation invocation) {
    // 检查传入的 invokers 服务提供者列表，若集合为空，则会抛出无提供者异常
    if (CollectionUtils.isEmpty(invokers)) {
        // 抛出的 RpcException 异常信息中，会有 No provider available 明显的关键字
        throw new RpcException(RpcException.NO_INVOKER_AVAILABLE_AFTER_FILTER, "Failed to invoke the method "
            + invocation.getMethodName() + " in the service " + getInterface().getName()
            + ". No provider available for the service " + getDirectory().getConsumerUrl().getServiceKey()
            + " from registry " + getDirectory().getUrl().getAddress()
            + " on the consumer " + NetUtils.getLocalHost()
            + " using the dubbo version " + Version.getVersion()
            + ". Please check if the providers have been started and registered.");
    }
}
```

注册节点变化可能原因：
1. 服务方动态注销了某个接口服务。
2. 服务方节点宕机了。
3. 服务方在代码中删掉了这个接口再启动，即永远不会再提供服务了。
4. 服务方修改了接口的类名、方法名。
5. 服务方未考虑版本兼容性，主动添加了 group、version 等参数。
6. ……

### 问题总结

分析了超时异常、无提供者异常，我们最终发现是因为某些提供方的 IP 节点宕机，但是还有些提供方的节点 IP 是正常提供服务的

可能是机房隔离性问题，某个机房的ip问题

### 定制Cluster扩展

可以提供一个中间扩展节点，调用转发服务代码。具体步骤**在定义一个 TransferClusterInvoker 类来继承 FailoverClusterInvoker，然后重写 checkInvokers** 
代码如下：

```java
public class TransferClusterInvoker<T> extends FailoverClusterInvoker<T> {
    // 按照父类 FailoverClusterInvoker 要求创建的构造方法
    public TransferClusterInvoker(Directory<T> directory) {
        super(directory);
    }
    // 重写父类 doInvoke 发起远程调用的接口
    @Override
    public Result doInvoke(Invocation invocation, List<Invoker<T>> invokers, LoadBalance loadbalance) throws RpcException {
        try {
            // 先完全按照父类的业务逻辑调用处理，无异常则直接将结果返回
            return super.doInvoke(invocation, invokers, loadbalance);
        } catch (RpcException e) {
            // 这里就进入了 RpcException 处理逻辑
            
            // 当调用发现无提供者异常描述信息时则向转发服务发起调用
            if (e.getMessage().toLowerCase().contains("no provider available")){
                // TODO 从 invocation 中拿到所有的参数，然后再处理调用转发服务的逻辑
                return doTransferInvoke(invocation);
            }
            // 如果不是无提供者异常，则不做任何处理，异常该怎么抛就怎么抛
            throw e;
        }
    }
}
```

然后需要新建一个Cluster类去触发上面的逻辑

```java

public class TransferCluster implements Cluster {
    // 返回自定义的 Invoker 调用器
    @Override
    public <T> Invoker<T> join(Directory<T> directory, boolean buildFilterChain) throws RpcException {
        return new TransferClusterInvoker<T>(directory);
    }
}
```

然后需要将这个类按照DUBBO SPI机制配置到 META-INF/dubbo/org.apache.dubbo.rpc.cluster.Cluster 文件中
```
transfer＝com.hmilyylimh.cloud.TransferCluster
```


### 应用

Dubbo 的集群扩展，相信你现在已经非常清楚了。Cluster 作为路由层，封装多个提供方的路由及负载均衡，并桥接注册中心以 Invoker 为中心发起调用，

第一，同机房请求无法连通时，可以考虑转发 HTTP 请求至可用提供者。
第二，内网本机访问测试环境无法连通时，可以转发请求至 HTTP 协议的接口，然后在接口中泛化调用各种 Dubbo 服务。
第三，如果针对接口的多个提供者需要做适应当前公司业务的筛选、剔除、负载均衡之类的诉求时，也是可以考虑集群扩展的。


## 地址

此文章为2月day8 学习笔记，内容来源于极客时间《[21｜调用流程：消费方的调用流程体系，你知道多少？ (geekbang.org)](https://time.geekbang.org/column/article/621733)》，推荐该课程
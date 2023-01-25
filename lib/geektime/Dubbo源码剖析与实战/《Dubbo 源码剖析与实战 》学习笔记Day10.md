
## 课程内容

### dubbo线程池相关

#### dubbo 同步调用出现的问题

1. BIO程序随着调用量的增加,导致性能问题
2. 复杂又有点耗时的功能,生产容易出现线程池耗尽的问题

#### 解决方式

1. 异步处理服务
	1. 显性异步: 分步异步去处理对应数据.将查询与返回分开.
		-  处理请求时共同的必经之路,在拦截处想办法拿到异步结果并返回
		- 使用netty网络模块,返回对应数据
	2. 隐性异步

##### 拦截并返回结果

结果存储方式:
1. ThreadLocal
2. 业务的上下文对象 👍

>异步问题，都需要考虑当前线程如何获取其他线程内数据
>⭐ : 使用Future的实现类`CompletableFuture.get()`

#### DUBBO源码级实现

![[Pasted image 20230126000524.png]]


1. 通过CAS创建CompletableFuture 对象,存储在`RpcContextAttachment`对象中
2. 通过调用`asyncContext.signalContextSwitch` 在异步线程中同步父线程的上下文信息
	-  只需要把这个所谓的 `asyncContext` 对象传入到子线程中，然后将 asyncContext 中的上下文信息充分拷贝到子线程中
3. 在异步线程中，用`asyncContext.write`写入到异步线程的上下文信息中,结果存入了`.CompletableFuture`对象中,只需要调用`CompletableFuture#get`就能获取对应结果
```java

// org.apache.dubbo.rpc.AsyncContextImpl#write
public void write(Object value) {
    if (isAsyncStarted() && stop()) {
        if (value instanceof Throwable) {
            Throwable bizExe = (Throwable) value;
            future.completeExceptionally(bizExe);
        } else {
            future.complete(value);
        }
    } else {
        throw new IllegalStateException("The async response has probably been wrote back by another thread, or the asyncContext has been closed.");
    }
}
```

#### 使用异步的场景

1. 对于一些 IO 耗时的操作，比较影响客户体验和使用性能的一些地方
2. 若某段业务逻辑开启异步执行后不太影响主线程的原有业务逻辑
3. 序上没有严格要求的业务逻辑

## 课程地址

[# 02｜异步化实践：莫名其妙出现线程池耗尽怎么办？](https://time.geekbang.org/column/article/611392)
---
title: Resilience4j-轻量级熔断框架 - 简书
url: https://www.jianshu.com/p/5531b66b777a
date: 2024-03-05 09:36:01
tags:
  - Resilience4j
  - 限流
  - java
---
## Resilience4j-轻量级熔断框架

## Resilience4j

## 简介

***Resilience4j***是一款轻量级，易于使用的容错库，其灵感来自于***Netflix Hystrix***，但是专为***Java*** **8**和函数式编程而设计。轻量级，因为库只使用了***Vavr***，它没有任何其他外部依赖下。相比之下，***Netflix Hystrix***对***Archaius***具有编译依赖性，***Archaius***具有更多的外部库依赖性，例如***Guava***和***Apache Commons Configuration***。

要使用***Resilience4j***，不需要引入所有依赖，只需要选择你需要的。

***Resilience4j***提供了以下的核心模块和拓展模块:

**核心模块：**

-   ***resilience4j-circuitbreaker: Circuit breaking***
-   ***resilience4j-ratelimiter: Rate limiting***
-   ***resilience4j-bulkhead: Bulkheading***
-   ***resilience4j-retry: Automatic retrying (sync and async)***
-   ***resilience4j-cache: Result caching***
-   ***resilience4j-timelimiter: Timeout handling***

## Circuitbreaker

### 简介

***CircuitBreaker***通过具有三种正常状态的有限状态机实现：***CLOSED***，***OPEN***和***HALF\_OPEN***以及两个特殊状态***DISABLED***和***FORCED\_OPEN***。当熔断器关闭时，所有的请求都会通过熔断器。如果失败率超过设定的阈值，熔断器就会从关闭状态转换到打开状态，这时所有的请求都会被拒绝。当经过一段时间后，熔断器会从打开状态转换到半开状态，这时仅有一定数量的请求会被放入，并重新计算失败率，如果失败率超过阈值，则变为打开状态，如果失败率低于阈值，则变为关闭状态。

![](https://upload-images.jianshu.io/upload_images/17742950-f8db8dc0ceb552d0.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/426/format/webp)

Circuitbreaker状态机

***Resilience4j***记录请求状态的数据结构和***Hystrix***不同，***Hystrix***是使用滑动窗口来进行存储的，而***Resilience4j***采用的是*Ring Bit Buffer*(环形缓冲区)。***Ring Bit Buffer***在内部使用***BitSet***这样的数据结构来进行存储，***BitSet***的结构如下图所示：

![](https://upload-images.jianshu.io/upload_images/17742950-9cedc9cd8d8d650f.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/222/format/webp)

环形缓冲区

每一次请求的成功或失败状态只占用一个***bit***位，与***boolean***数组相比更节省内存。***BitSet***使用***long\[\]***数组来存储这些数据，意味着**16**个值(***64bit***)的数组可以存储**1024**个调用状态。

计算失败率需要填满环形缓冲区。例如，如果环形缓冲区的大小为**10**，则必须至少请求满**10**次，才会进行故障率的计算，如果仅仅请求了**9**次，即使**9**个请求都失败，熔断器也不会打开。但是***CLOSE***状态下的缓冲区大小设置为**10**并不意味着只会进入**10**个 请求，在熔断器打开之前的所有请求都会被放入。

当故障率高于设定的阈值时，熔断器状态会从由***CLOSE***变为***OPEN***。这时所有的请求都会抛出***CallNotPermittedException***异常。当经过一段时间后，熔断器的状态会从***OPEN***变为***HALF\_OPEN***，***HALF\_OPEN***状态下同样会有一个***Ring Bit Buffer***，用来计算***HALF\_OPEN***状态下的故障率，如果高于配置的阈值，会转换为***OPEN***，低于阈值则装换为***CLOSE***。与***CLOSE***状态下的缓冲区不同的地方在于，***HALF\_OPEN***状态下的缓冲区大小会限制请求数，只有缓冲区大小的请求数会被放入。

除此以外，熔断器还会有两种特殊状态：***DISABLED***（始终允许访问）和***FORCED\_OPEN***（始终拒绝访问）。这两个状态不会生成熔断器事件（除状态装换外），并且不会记录事件的成功或者失败。退出这两个状态的唯一方法是触发状态转换或者重置熔断器。

熔断器关于线程安全的保证措施有以下几个部分：

-   熔断器的状态使用***AtomicReference***保存的
-   更新熔断器状态是通过无状态的函数或者原子操作进行的
-   更新事件的状态用***synchronized***关键字保护

意味着同一时间只有一个线程能够修改熔断器状态或者记录事件的状态。

### 可配置参数

配置参数

默认值

描述

failureRateThreshold

50

熔断器关闭状态和半开状态使用的同一个失败率阈值

ringBufferSizeInHalfOpenState

10

熔断器半开状态的缓冲区大小，会限制线程的并发量，例如缓冲区为10则每次只会允许10个请求调用后端服务

ringBufferSizeInClosedState

100

熔断器关闭状态的缓冲区大小，不会限制线程的并发量，在熔断器发生状态转换前所有请求都会调用后端服务

waitDurationInOpenState

60(s)

熔断器从打开状态转变为半开状态等待的时间

automaticTransitionFromOpenToHalfOpenEnabled

false

如果置为true，当等待时间结束会自动由打开变为半开，若置为false，则需要一个请求进入来触发熔断器状态转换

recordExceptions

empty

需要记录为失败的异常列表

ignoreExceptions

empty

需要忽略的异常列表

recordFailure

throwable -> true

自定义的谓词逻辑用于判断异常是否需要记录或者需要忽略，默认所有异常都进行记录

### 测试前准备

#### pom.xml

测试使用的***IDE***为***idea***，使用的***springboot***进行学习测试，首先引入***maven***依赖：

```
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-spring-boot</artifactId>
    <version>0.9.0</version>
</dependency>
```

***resilience4j-spring-boot***集成了***circuitbeaker***、***retry***、***bulkhead***、***ratelimiter***几个模块，因为后续还要学习其他模块，就直接引入***resilience4j-spring-boot***依赖。

#### application.yml配置

```
resilience4j:
  circuitbreaker:
    configs:
      default:
        ringBufferSizeInClosedState: 5 # 熔断器关闭时的缓冲区大小
        ringBufferSizeInHalfOpenState: 2 # 熔断器半开时的缓冲区大小
        waitDurationInOpenState: 10000 # 熔断器从打开到半开需要的时间
        failureRateThreshold: 60 # 熔断器打开的失败阈值
        eventConsumerBufferSize: 10 # 事件缓冲区大小
        registerHealthIndicator: true # 健康监测
        automaticTransitionFromOpenToHalfOpenEnabled: false # 是否自动从打开到半开，不需要触发
        recordFailurePredicate:    com.example.resilience4j.exceptions.RecordFailurePredicate # 谓词设置异常是否为失败
        recordExceptions: # 记录的异常
          - com.example.resilience4j.exceptions.BusinessBException
          - com.example.resilience4j.exceptions.BusinessAException
        ignoreExceptions: # 忽略的异常
          - com.example.resilience4j.exceptions.BusinessAException
    instances:
      backendA:
        baseConfig: default
        waitDurationInOpenState: 5000
        failureRateThreshold: 20
      backendB:
        baseConfig: default
```

可以配置多个熔断器实例，使用不同配置或者覆盖配置。

#### 需要保护的后端服务

以一个查找用户列表的后端服务为例，利用熔断器保护该服务。

```
interface RemoteService {
    List<User> process() throws TimeoutException, InterruptedException;
}
```

#### 连接器调用该服务

这是调用远端服务的连接器，我们通过调用连接器中的方法来调用后端服务。

```
public RemoteServiceConnector{
    public List<User> process() throws TimeoutException, InterruptedException {
        List<User> users;
        users = remoteServic.process();
        return users;
    }
}
```

#### 用于监控熔断器状态及事件的工具类

要想学习各个配置项的作用，需要获取特定时候的熔断器状态，写一个工具类：

```
@Log4j2
public class CircuitBreakerUtil {

    /**
     * @Description: 获取熔断器的状态
     */
    public static void getCircuitBreakerStatus(String time, CircuitBreaker circuitBreaker){
        CircuitBreaker.Metrics metrics = circuitBreaker.getMetrics();
        // Returns the failure rate in percentage.
        float failureRate = metrics.getFailureRate();
        // Returns the current number of buffered calls.
        int bufferedCalls = metrics.getNumberOfBufferedCalls();
        // Returns the current number of failed calls.
        int failedCalls = metrics.getNumberOfFailedCalls();
        // Returns the current number of successed calls.
        int successCalls = metrics.getNumberOfSuccessfulCalls();
        // Returns the max number of buffered calls.
        int maxBufferCalls = metrics.getMaxNumberOfBufferedCalls();
        // Returns the current number of not permitted calls.
        long notPermittedCalls = metrics.getNumberOfNotPermittedCalls();

        log.info(time + "state=" +circuitBreaker.getState() + " , metrics[ failureRate=" + failureRate +
                ", bufferedCalls=" + bufferedCalls +
                ", failedCalls=" + failedCalls +
                ", successCalls=" + successCalls +
                ", maxBufferCalls=" + maxBufferCalls +
                ", notPermittedCalls=" + notPermittedCalls +
                " ]"
        );
    }

    /**
     * @Description: 监听熔断器事件
     */
    public static void addCircuitBreakerListener(CircuitBreaker circuitBreaker){
        circuitBreaker.getEventPublisher()
                .onSuccess(event -> log.info("服务调用成功：" + event.toString()))
                .onError(event -> log.info("服务调用失败：" + event.toString()))
                .onIgnoredError(event -> log.info("服务调用失败，但异常被忽略：" + event.toString()))
                .onReset(event -> log.info("熔断器重置：" + event.toString()))
                .onStateTransition(event -> log.info("熔断器状态改变：" + event.toString()))
                .onCallNotPermitted(event -> log.info(" 熔断器已经打开：" + event.toString()))
        ;
    }
```

### 调用方法

***CircuitBreaker***目前支持两种方式调用，一种是程序式调用，一种是***AOP***使用注解的方式调用。

#### 程序式的调用方法

在***CircuitService***中先注入注册器，然后用注册器通过熔断器名称获取熔断器。如果不需要使用降级函数，可以直接调用熔断器的***executeSupplier***方法或***executeCheckedSupplier***方法：

```
public class CircuitBreakerServiceImpl{
    
    @Autowired
    private CircuitBreakerRegistry circuitBreakerRegistry;

    public List<User> circuitBreakerNotAOP() throws Throwable {
        CircuitBreaker circuitBreaker = circuitBreakerRegistry.circuitBreaker("backendA");
        CircuitBreakerUtil.getCircuitBreakerStatus("执行开始前：", circuitBreaker);
        circuitBreaker.executeCheckedSupplier(remotServiceConnector::process);
    }
}
```

如果需要使用降级函数，则要使用***decorate***包装服务的方法，再使用***Try.of().recover()***进行降级处理，同时也可以根据不同的异常使用不同的降级方法：

```
public class CircuitBreakerServiceImpl {
    
    @Autowired
    private RemoteServiceConnector remoteServiceConnector;
    
    @Autowired
    private CircuitBreakerRegistry circuitBreakerRegistry;

    public List<User> circuitBreakerNotAOP(){
        // 通过注册器获取熔断器的实例
        CircuitBreaker circuitBreaker = circuitBreakerRegistry.circuitBreaker("backendA");
        CircuitBreakerUtil.getCircuitBreakerStatus("执行开始前：", circuitBreaker);
        // 使用熔断器包装连接器的方法
        CheckedFunction0<List<User>> checkedSupplier = CircuitBreaker.
            decorateCheckedSupplier(circuitBreaker, remoteServiceConnector::process);
        // 使用Try.of().recover()调用并进行降级处理
        Try<List<User>> result = Try.of(checkedSupplier).
                    recover(CallNotPermittedException.class, throwable -> {
                        log.info("熔断器已经打开，拒绝访问被保护方法~");
                        CircuitBreakerUtil
                        .getCircuitBreakerStatus("熔断器打开中:", circuitBreaker);
                        List<User> users = new ArrayList();
                        return users;
                    })
                    .recover(throwable -> {
                        log.info(throwable.getLocalizedMessage() + ",方法被降级了~~");
                        CircuitBreakerUtil
                        .getCircuitBreakerStatus("降级方法中:",circuitBreaker);
                        List<User> users = new ArrayList();
                        return users;
                    });
            CircuitBreakerUtil.getCircuitBreakerStatus("执行结束后：", circuitBreaker);
            return result.get();
    }
}
```

#### AOP式的调用方法

首先在连接器方法上使用***@CircuitBreaker(name="",fallbackMethod="")***注解，其中***name***是要使用的熔断器的名称，***fallbackMethod***是要使用的降级方法，降级方法必须和原方法放在同一个类中，且降级方法的返回值需要和原方法相同，输入参数需要添加额外的***exception***参数，类似这样：

```
public RemoteServiceConnector{
    
    @CircuitBreaker(name = "backendA", fallbackMethod = "fallBack")
    public List<User> process() throws TimeoutException, InterruptedException {
        List<User> users;
        users = remoteServic.process();
        return users;
    }
    
    private List<User> fallBack(Throwable throwable){
        log.info(throwable.getLocalizedMessage() + ",方法被降级了~~");
        CircuitBreakerUtil.getCircuitBreakerStatus("降级方法中:", circuitBreakerRegistry.circuitBreaker("backendA"));
        List<User> users = new ArrayList();
        return users;
    }
    
    private List<User> fallBack(CallNotPermittedException e){
        log.info("熔断器已经打开，拒绝访问被保护方法~");
        CircuitBreakerUtil.getCircuitBreakerStatus("熔断器打开中:", circuitBreakerRegistry.circuitBreaker("backendA"));
        List<User> users = new ArrayList();
        return users;
    }
    
} 
```

可使用多个降级方法，保持方法名相同，同时满足的条件的降级方法会触发最接近的一个（这里的接近是指类型的接近，先会触发离它最近的子类异常），例如如果***process()***方法抛出***CallNotPermittedException***，将会触发***fallBack(CallNotPermittedException e)***方法而不会触发***fallBack(Throwable throwable)***方法。

之后直接调用方法就可以了：

```
public class CircuitBreakerServiceImpl {
    
    @Autowired
    private RemoteServiceConnector remoteServiceConnector;
    
    @Autowired
    private CircuitBreakerRegistry circuitBreakerRegistry;
    
    public List<User> circuitBreakerAOP() throws TimeoutException, InterruptedException {
        CircuitBreakerUtil
            .getCircuitBreakerStatus("执行开始前：",circuitBreakerRegistry.circuitBreaker("backendA"));
        List<User> result = remoteServiceConnector.process();
        CircuitBreakerUtil
            .getCircuitBreakerStatus("执行结束后：", circuitBreakerRegistry.circuitBreaker("backendA"));
        return result;
    }
}
```

### 使用测试

接下来进入测试，首先我们定义了两个异常，异常A同时在黑白名单中，异常B只在黑名单中：

```
recordExceptions: # 记录的异常
    - com.example.resilience4j.exceptions.BusinessBException
    - com.example.resilience4j.exceptions.BusinessAException
ignoreExceptions: # 忽略的异常
    - com.example.resilience4j.exceptions.BusinessAException
```

然后对被保护的后端接口进行如下的实现：

```
public class RemoteServiceImpl implements RemoteService {
    
    private static AtomicInteger count = new AtomicInteger(0);

    public List<User> process() {
        int num = count.getAndIncrement();
        log.info("count的值 = " + num);
        if (num % 4 == 1){
            throw new BusinessAException("异常A，不需要被记录");
        }
        if (num % 4 == 2 || num % 4 == 3){
            throw new BusinessBException("异常B，需要被记录");
        }
        log.info("服务正常运行，获取用户列表");
        // 模拟数据库的正常查询
        return repository.findAll();
    }
}
```

使用***CircuitBreakerServiceImpl***中的***AOP***或者程序式调用方法进行单元测试，循环调用**10**次：

```
public class CircuitBreakerServiceImplTest{
    
    @Autowired
    private CircuitBreakerServiceImpl circuitService;
    
    @Test
    public void circuitBreakerTest() {
        for (int i=0; i<10; i++){
            // circuitService.circuitBreakerAOP();
            circuitService.circuitBreakerNotAOP();
        }
    }
}
```

看下运行结果：

```
执行开始前：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=0, failedCalls=0, successCalls=0, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 0
服务正常运行，获取用户列表
执行结束后：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, 
执行开始前：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 1
异常A，不需要被记录,方法被降级了~~
降级方法中:state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行结束后：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 2
异常B，需要被记录,方法被降级了~~
降级方法中:state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=2, failedCalls=1, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行结束后：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=2, failedCalls=1, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=2, failedCalls=1, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 3
异常B，需要被记录,方法被降级了~~
降级方法中:state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=3, failedCalls=2, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行结束后：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=3, failedCalls=2, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=3, failedCalls=2, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 4
服务正常运行，获取用户列表
执行结束后：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=4, failedCalls=2, successCalls=2, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=4, failedCalls=2, successCalls=2, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 5
异常A，不需要被记录,方法被降级了~~
降级方法中:state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=4, failedCalls=2, successCalls=2, maxBufferCalls=5, notPermittedCalls=0 ]
执行结束后：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=4, failedCalls=2, successCalls=2, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=4, failedCalls=2, successCalls=2, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 6
异常B，需要被记录,方法被降级了~~
降级方法中:state=OPEN , metrics[ failureRate=60.0, bufferedCalls=5, failedCalls=3, successCalls=2, maxBufferCalls=5, notPermittedCalls=0 ]
执行结束后：state=OPEN , metrics[ failureRate=60.0, bufferedCalls=5, failedCalls=3, successCalls=2, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=OPEN , metrics[ failureRate=60.0, bufferedCalls=5, failedCalls=3, successCalls=2, maxBufferCalls=5, notPermittedCalls=0 ]
熔断器已经打开，拒绝访问被保护方法~
熔断器打开中:state=OPEN , metrics[ failureRate=60.0, bufferedCalls=5, failedCalls=3, successCalls=2, maxBufferCalls=5, notPermittedCalls=1 ]
执行结束后：state=OPEN , metrics[ failureRate=60.0, bufferedCalls=5, failedCalls=3, successCalls=2, maxBufferCalls=5, notPermittedCalls=1 ]
```

注意到异常***A***发生的前后***bufferedCalls***、***failedCalls***、***successCalls***三个参数的值都没有没有发生变化，说明白名单的优先级高于黑名单，源码中也有提到***Ignoring an exception has priority over recording an exception***：

```
/**
* @see #ignoreExceptions(Class[]) ). Ignoring an exception has priority over recording an exception.
* <p>
* Example:
* recordExceptions(Throwable.class) and ignoreExceptions(RuntimeException.class)
* would capture all Errors and checked Exceptions, and ignore unchecked
* <p>
*/
```

同时也可以看出白名单所谓的忽略，是指不计入缓冲区中（即不算成功也不算失败），有降级方法会调用降级方法，没有降级方法会抛出异常，和其他异常无异。

```
执行开始前：state=OPEN , metrics[ failureRate=60.0, bufferedCalls=5, failedCalls=3, successCalls=2, maxBufferCalls=5, notPermittedCalls=0 ]
熔断器已经打开，拒绝访问被保护方法~
熔断器打开中:state=OPEN , metrics[ failureRate=60.0, bufferedCalls=5, failedCalls=3, successCalls=2, maxBufferCalls=5, notPermittedCalls=1 ]
执行结束后：state=OPEN , metrics[ failureRate=60.0, bufferedCalls=5, failedCalls=3, successCalls=2, maxBufferCalls=5, notPermittedCalls=1 ]
```

当环形缓冲区大小被填满时会计算失败率，这时请求会被拒绝获取不到***count***的值，且***notPermittedCalls***会增加。

---

接下来我们实验一下多线程下熔断器关闭和熔断器半开两种情况下缓冲环的区别，我们先开**15**个线程进行调用测试熔断器关闭时的缓冲环，熔断之后等***10s***再开**15**个线程进行调用测试熔断器半开时的缓冲环：

```
public class CircuitBreakerServiceImplTest{
    
    @Autowired
    private CircuitBreakerServiceImpl circuitService;
    
    @Test
    public void circuitBreakerThreadTest() throws InterruptedException {
        ExecutorService pool = Executors.newCachedThreadPool();
        for (int i=0; i<15; i++){
            pool.submit(
                // circuitService::circuitBreakerAOP
                circuitService::circuitBreakerNotAOP);
        }
        pool.shutdown();

        while (!pool.isTerminated());

        Thread.sleep(10000);
        log.info("熔断器状态已转为半开");
        pool = Executors.newCachedThreadPool();
        for (int i=0; i<15; i++){
            pool.submit(
                // circuitService::circuitBreakerAOP
                circuitService::circuitBreakerNotAOP);
        }
        pool.shutdown();

        while (!pool.isTerminated());
        for (int i=0; i<10; i++){
            
        }
    }
}
```

前**15**个线程都通过了熔断器，由于正常返回需要查数据库，所以会慢很多，失败率很快就达到了**100%**，而且观察到如下的记录：

```
异常B，需要被记录,方法被降级了~~
降级方法中:state=OPEN , metrics[ failureRate=100.0, bufferedCalls=5, failedCalls=5, successCalls=0, maxBufferCalls=5, notPermittedCalls=0 ]
```

可以看出，虽然熔断器已经打开了，可是异常***B***还是进入了降级方法，抛出的异常不是***notPermittedCalls***数量为**0**，说明在熔断器转换成打开之前所有请求都通过了熔断器，缓冲环不会控制线程的并发。

```
执行结束后：state=OPEN , metrics[ failureRate=80.0, bufferedCalls=5, failedCalls=4, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行结束后：state=OPEN , metrics[ failureRate=60.0, bufferedCalls=5, failedCalls=3, successCalls=2, maxBufferCalls=5, notPermittedCalls=0 ]
执行结束后：state=OPEN , metrics[ failureRate=40.0, bufferedCalls=5, failedCalls=2, successCalls=3, maxBufferCalls=5, notPermittedCalls=0 ]
执行结束后：state=OPEN , metrics[ failureRate=20.0, bufferedCalls=5, failedCalls=1, successCalls=4, maxBufferCalls=5, notPermittedCalls=0 ]
```

同时以上几条正常执行的服务完成后，熔断器的失败率在下降，说明熔断器打开状态下还是会计算失败率，由于环形缓冲区大小为**5**，初步推断成功的状态会依次覆盖最开始的几个状态，所以得到了上述结果。

接下来分析后**15**个线程的结果

```
熔断器状态已转为半开
执行开始前：state=OPEN , metrics[ failureRate=0.0, bufferedCalls=5, failedCalls=0, successCalls=5, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=OPEN , metrics[ failureRate=0.0, bufferedCalls=5, failedCalls=0, successCalls=5, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=OPEN , metrics[ failureRate=0.0, bufferedCalls=5, failedCalls=0, successCalls=5, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=OPEN , metrics[ failureRate=0.0, bufferedCalls=5, failedCalls=0, successCalls=5, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=OPEN , metrics[ failureRate=0.0, bufferedCalls=5, failedCalls=0, successCalls=5, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=OPEN , metrics[ failureRate=0.0, bufferedCalls=5, failedCalls=0, successCalls=5, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 16
服务正常运行，获取用户列表
执行开始前：state=OPEN , metrics[ failureRate=0.0, bufferedCalls=5, failedCalls=0, successCalls=5, maxBufferCalls=5, notPermittedCalls=0 ]
熔断器状态改变：2019-07-29T17:19:19.959+08:00[Asia/Shanghai]: CircuitBreaker 'backendA' changed state from OPEN to HALF_OPEN
count的值 = 18
count的值 = 17
服务正常运行，获取用户列表
count的值 = 19
count的值 = 15
```

熔断器状态从打开到半开我设置的是***5s***，前**15**个线程调用之后我等待了***10s***，熔断器应该已经变为半开了，但是执行开始前熔断器的状态却是***OPEN***，这是因为默认的配置项***automaticTransitionFromOpenToHalfOpenEnabled=false***，时间到了也不会自动转换，需要有新的请求来触发熔断器的状态转换。同时我们发现，好像状态改变后还是进了超过***4***个请求，似乎半开状态的环并不能限制线程数？这是由于这些进程是在熔断器打开时一起进来的。为了更好的观察环半开时候环大小是否限制线程数，我们修改一下配置：

```
resilience4j:
  circuitbreaker:
    configs:
      myDefault:
        automaticTransitionFromOpenToHalfOpenEnabled: true # 是否自动从打开到半开
```

我们再试一次：

```
熔断器状态已转为半开
执行开始前：state=HALF_OPEN , metrics[ failureRate=-1.0, bufferedCalls=0, failedCalls=0, successCalls=0, maxBufferCalls=4, notPermittedCalls=0 ]
执行开始前：state=HALF_OPEN , metrics[ failureRate=-1.0, bufferedCalls=0, failedCalls=0, successCalls=0, maxBufferCalls=4, notPermittedCalls=0 ]
执行开始前：state=HALF_OPEN , metrics[ failureRate=-1.0, bufferedCalls=0, failedCalls=0, successCalls=0, maxBufferCalls=4, notPermittedCalls=0 ]
count的值 = 15
count的值 = 16
服务正常运行，获取用户列表
 异常B，需要被记录,方法被降级了~~
降级方法中:state=HALF_OPEN , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=1, successCalls=0, maxBufferCalls=4, notPermittedCalls=0 ]
执行结束后：state=HALF_OPEN , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=1, successCalls=0, maxBufferCalls=4, notPermittedCalls=0 ]
count的值 = 17
异常A，不需要被记录,方法被降级了~~
降级方法中:state=HALF_OPEN , metrics[ failureRate=-1.0, bufferedCalls=2, failedCalls=2, successCalls=0, maxBufferCalls=4, notPermittedCalls=0 ]
执行开始前：state=HALF_OPEN , metrics[ failureRate=-1.0, bufferedCalls=2, failedCalls=2, successCalls=0, maxBufferCalls=4, notPermittedCalls=0 ]
count的值 = 18
执行开始前：state=HALF_OPEN , metrics[ failureRate=-1.0, bufferedCalls=2, failedCalls=2, successCalls=0, maxBufferCalls=4, notPermittedCalls=0 ]
异常B，需要被记录,方法被降级了~~
降级方法中:state=HALF_OPEN , metrics[ failureRate=-1.0, bufferedCalls=3, failedCalls=3, successCalls=0, maxBufferCalls=4, notPermittedCalls=0 ]
执行结束后：state=HALF_OPEN , metrics[ failureRate=-1.0, bufferedCalls=3, failedCalls=3, successCalls=0, maxBufferCalls=4, notPermittedCalls=0 ]
熔断器已经打开：2019-07-29T17:36:14.189+08:00[Asia/Shanghai]: CircuitBreaker 'backendA' recorded a call which was not permitted.
执行开始前：state=HALF_OPEN , metrics[ failureRate=-1.0, bufferedCalls=2, failedCalls=2, successCalls=0, maxBufferCalls=4, notPermittedCalls=0 ]
执行结束后：state=HALF_OPEN , metrics[ failureRate=-1.0, bufferedCalls=2, failedCalls=2, successCalls=0, maxBufferCalls=4, notPermittedCalls=0 ]
熔断器已经打开，拒绝访问被保护方法~
```

结果只有***4***个请求进去了，可以看出虽然熔断器状态还是半开，但是已经熔断了，说明在半开状态下，超过环大小的请求会被直接拒绝。

综上，***circuitbreaker***的机制已经被证实，且十分清晰，以下为几个需要注意的点：

-   失败率的计算必须等环装满才会计算
-   白名单优先级高于黑名单且白名单上的异常会被忽略，不会占用缓冲环位置，即不会计入失败率计算
-   熔断器打开时同样会计算失败率，当状态转换为半开时重置为**\-1**
-   只要出现异常都可以调用降级方法，不论是在白名单还是黑名单
-   熔断器的缓冲环有两个，一个关闭时的缓冲环，一个打开时的缓冲环
-   熔断器关闭时，直至熔断器状态转换前所有请求都会通过，不会受到限制
-   熔断器半开时，限制请求数为缓冲环的大小，其他请求会等待
-   熔断器从打开到半开的转换默认还需要请求进行触发，也可通过***automaticTransitionFromOpenToHalfOpenEnabled=true***设置为自动触发

## TimeLimiter

### 简介

与***Hystrix***不同，***Resilience4j***将超时控制器从熔断器中独立出来，成为了一个单独的组件，主要的作用就是对方法调用进行超时控制。实现的原理和***Hystrix***相似，都是通过调用***Future***的***get***方法来进行超时控制。

### 可配置参数

配置参数

默认值

描述

timeoutDuration

1(s)

超时时间限定

cancelRunningFuture

true

当超时时是否关闭取消线程

### 测试前准备

#### pom.xml

```
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-timelimiter</artifactId>
    <version>0.16.0</version>
</dependency>
```

***TimeLimiter***没有整合进***resilience4j-spring-boot***中，需要单独添加依赖

#### application.yml配置

```
timelimiter:
    timeoutDuration: 3000 # 超时时长
    cancelRunningFuture: true # 发生异常是否关闭线程
```

***TimeLimiter***没有配置自动注入，需要自己进行注入，写下面两个文件进行配置自动注入：

#### TimeLimiterProperties

用于将***application.yml***中的配置转换为***TimeLimiterProperties***对象：

```
@Data
@Component
@ConfigurationProperties(prefix = "resilience4j.timelimiter")
public class TimeLimiterProperties {

    private Duration timeoutDuration;

    private boolean cancelRunningFuture;
}
```

#### TimeLimiterConfiguration

将***TimeLimiterProperties***对象写入到***TimeLimiter***的配置中：

```
@Configuration
public class TimeLimiterConfiguration {

    @Autowired
    private TimeLimiterProperties timeLimiterProperties;

    @Bean
    public TimeLimiter timeLimiter(){
        return TimeLimiter.of(timeLimiterConfig());
    }

    private TimeLimiterConfig timeLimiterConfig(){
        return TimeLimiterConfig.custom()
                .timeoutDuration(timeLimiterProperties.getTimeoutDuration())
                .cancelRunningFuture(timeLimiterProperties.isCancelRunningFuture()).build();
    }
}
```

### 调用方法

还是以之前查询用户列表的后端服务为例。***TimeLimiter***目前仅支持程序式调用，还不能使用***AOP***的方式调用。

因为***TimeLimiter***通常与***CircuitBreaker***联合使用，很少单独使用，所以直接介绍联合使用的步骤。

***TimeLimiter***没有注册器，所以通过***@Autowired***注解自动注入依赖直接使用，因为***TimeLimter***是基于***Future***的***get***方法的，所以需要创建线程池，然后通过线程池的***submit***方法获取***Future***对象：

```
public class CircuitBreakerServiceImpl {
    
    @Autowired
    private RemoteServiceConnector remoteServiceConnector;
    
    @Autowired
    private CircuitBreakerRegistry circuitBreakerRegistry;
    
    @Autowired
    private TimeLimiter timeLimiter;

    public List<User> circuitBreakerTimeLimiter(){
        // 通过注册器获取熔断器的实例
        CircuitBreaker circuitBreaker = circuitBreakerRegistry.circuitBreaker("backendA");
        CircuitBreakerUtil.getCircuitBreakerStatus("执行开始前：", circuitBreaker);
        // 创建单线程的线程池
        ExecutorService pool = Executors.newSingleThreadExecutor();
        //将被保护方法包装为能够返回Future的supplier函数
        Supplier<Future<List<User>>> futureSupplier = () -> pool.submit(remoteServiceConnector::process);
        // 先用限时器包装，再用熔断器包装
        Callable<List<User>> restrictedCall = TimeLimiter.decorateFutureSupplier(timeLimiter, futureSupplier);
        Callable<List<User>> chainedCallable = CircuitBreaker.decorateCallable(circuitBreaker, restrictedCall);
        // 使用Try.of().recover()调用并进行降级处理
        Try<List<User>> result = Try.of(chainedCallable::call)
            .recover(CallNotPermittedException.class, throwable ->{
                log.info("熔断器已经打开，拒绝访问被保护方法~");
                CircuitBreakerUtil.getCircuitBreakerStatus("熔断器打开中", circuitBreaker);
                List<User> users = new ArrayList();
                return users;
            })
            .recover(throwable -> {
                log.info(throwable.getLocalizedMessage() + ",方法被降级了~~");
                CircuitBreakerUtil.getCircuitBreakerStatus("降级方法中:",circuitBreaker);
                List<User> users = new ArrayList();
                return users;
            });
        CircuitBreakerUtil.getCircuitBreakerStatus("执行结束后：", circuitBreaker);
        return result.get();
    }
}
```

### 使用测试

异常***A***和***B***在***application.yml***文件中没有修改：

```
recordExceptions: # 记录的异常
    - com.example.resilience4j.exceptions.BusinessBException
    - com.example.resilience4j.exceptions.BusinessAException
ignoreExceptions: # 忽略的异常
    - com.example.resilience4j.exceptions.BusinessAException
```

使用另一个远程服务接口的实现，将***num%4==3***的情况让线程休眠***5s***，大于我们***TimeLimiter***的限制时间：

```
public class RemoteServiceImpl implements RemoteService {
    
    private static AtomicInteger count = new AtomicInteger(0);

    public List<User> process() {
        int num = count.getAndIncrement();
        log.info("count的值 = " + num);
        if (num % 4 == 1){
            throw new BusinessAException("异常A，不需要被记录");
        }
        if (num % 4 == 2){
            throw new BusinessBException("异常B，需要被记录");
        }
        if (num % 4 == 3){
            Thread.sleep(5000);
        }
        log.info("服务正常运行，获取用户列表");
        // 模拟数据库的正常查询
        return repository.findAll();
    }
}
```

把调用方法进行单元测试，循环**10**遍：

```
public class CircuitBreakerServiceImplTest{
    
    @Autowired
    private CircuitBreakerServiceImpl circuitService;
    
    @Test
    public void circuitBreakerTimeLimiterTest() {
        for (int i=0; i<10; i++){
            circuitService.circuitBreakerTimeLimiter();
        }
    }
}
```

看下运行结果：

```
执行开始前：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=0, failedCalls=0, successCalls=0, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 0
服务正常运行，获取用户列表
执行结束后：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 1
com.example.resilience4j.exceptions.BusinessAException: 异常A，不需要被记录,方法被降级了~~
降级方法中:state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行结束后：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 2
com.example.resilience4j.exceptions.BusinessBException: 异常B，需要被记录,方法被降级了~~
降级方法中:state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行结束后：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行开始前：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 3
null,方法被降级了~~
降级方法中:state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行结束后：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
```

发现熔断器任何异常和超时都没有失败。。完全不会触发熔断，这是为什么呢？我们把异常***toString()***看一下：

```
java.util.concurrent.ExecutionException: com.example.resilience4j.exceptions.BusinessBException: 异常B，需要被记录,方法被降级了~~
java.util.concurrent.TimeoutException,方法被降级了~~
```

这下原因就很明显了，线程池会将线程中的任何异常包装为***ExecutionException***，而熔断器没有把异常解包，由于我们设置了黑名单，而熔断器又没有找到黑名单上的异常，所以失效了。这是一个已知的***bug***，会在下个版本(**0.16.0**之后)中修正，目前来说如果需要同时使用***TimeLimiter***和***CircuitBreaker***的话，黑白名单的设置是不起作用的，需要自定义自己的谓词逻辑，并在***test()***方法中将异常解包进行判断，比如像下面这样：

```
public class RecordFailurePredicate implements Predicate<Throwable> {

    @Override
    public boolean test(Throwable throwable) {
        if (throwable.getCause() instanceof BusinessAException) return false;
        else return true;
    }
}
```

然后在***application.yml***文件中指定这个类作为判断类：

```
circuitbreaker:
    configs:
      default:
        recordFailurePredicate: com.example.resilience4j.predicate.RecordFailurePredicate
```

就能自定义自己的黑白名单了，我们再运行一次试试：

```
java.util.concurrent.TimeoutException,方法被降级了~~
降级方法中:state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=3, failedCalls=2, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
执行结束后：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=3, failedCalls=2, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
```

可以看出，***TimeLimiter***已经生效了，同时***CircuitBreaker***也正常工作。

### Note:

最新版0.17.0，该bug已经修复，黑白名单可以正常使用。

## Retry

### 简介

同熔断器一样，重试组件也提供了注册器，可以通过注册器获取实例来进行重试，同样可以跟熔断器配合使用。

### 可配置参数

配置参数

默认值

描述

maxAttempts

3

最大重试次数

waitDuration

500\[ms\]

固定重试间隔

intervalFunction

numberOfAttempts -> waitDuration

用来改变重试时间间隔，可以选择指数退避或者随机时间间隔

retryOnResultPredicate

result -> false

自定义结果重试规则，需要重试的返回true

retryOnExceptionPredicate

throwable -> true

自定义异常重试规则，需要重试的返回true

retryExceptions

empty

需要重试的异常列表

ignoreExceptions

empty

需要忽略的异常列表

### 测试前准备

#### pom.xml

不需要引入新的依赖，已经集成在***resilience4j-spring-boot***中了

#### application.yml配置

```
resilience4j:
  retry:
    configs:
      default:
      maxRetryAttempts: 3
      waitDuration: 10s
      enableExponentialBackoff: true    # 是否允许使用指数退避算法进行重试间隔时间的计算
      expontialBackoffMultiplier: 2     # 指数退避算法的乘数
      enableRandomizedWait: false       # 是否允许使用随机的重试间隔
      randomizedWaitFactor: 0.5         # 随机因子
      resultPredicate: com.example.resilience4j.predicate.RetryOnResultPredicate    
      retryExceptionPredicate: com.example.resilience4j.predicate.RetryOnExceptionPredicate
      retryExceptions:
        - com.example.resilience4j.exceptions.BusinessBException
        - com.example.resilience4j.exceptions.BusinessAException
        - io.github.resilience4j.circuitbreaker.CallNotPermittedException
      ignoreExceptions:
        - io.github.resilience4j.circuitbreaker.CallNotPermittedException
      instances:
        backendA:
          baseConfig: default
          waitDuration: 5s
        backendB:
          baseConfig: default
          maxRetryAttempts: 2   
```

***application.yml***可以配置的参数多出了几个***enableExponentialBackoff***、***expontialBackoffMultiplier***、***enableRandomizedWait***、***randomizedWaitFactor***，分别代表是否允许指数退避间隔时间，指数退避的乘数、是否允许随机间隔时间、随机因子，注意指数退避和随机间隔不能同时启用。

#### 用于监控重试组件状态及事件的工具类

同样为了监控重试组件，写一个工具类：

```
@Log4j2
public class RetryUtil {

    /**
     * @Description: 获取重试的状态
     */
    public static void getRetryStatus(String time, Retry retry){
        Retry.Metrics metrics = retry.getMetrics();
        long failedRetryNum = metrics.getNumberOfFailedCallsWithRetryAttempt();
        long failedNotRetryNum = metrics.getNumberOfFailedCallsWithoutRetryAttempt();
        long successfulRetryNum = metrics.getNumberOfSuccessfulCallsWithRetryAttempt();
        long successfulNotyRetryNum = metrics.getNumberOfSuccessfulCallsWithoutRetryAttempt();

        log.info(time + "state=" + " metrics[ failedRetryNum=" + failedRetryNum +
                ", failedNotRetryNum=" + failedNotRetryNum +
                ", successfulRetryNum=" + successfulRetryNum +
                ", successfulNotyRetryNum=" + successfulNotyRetryNum +
                " ]"
        );
    }

    /**
     * @Description: 监听重试事件
     */
    public static void addRetryListener(Retry retry){
        retry.getEventPublisher()
                .onSuccess(event -> log.info("服务调用成功：" + event.toString()))
                .onError(event -> log.info("服务调用失败：" + event.toString()))
                .onIgnoredError(event -> log.info("服务调用失败，但异常被忽略：" + event.toString()))
                .onRetry(event -> log.info("重试：第" + event.getNumberOfRetryAttempts() + "次"))
        ;
    }
}
```

### 调用方法

还是以之前查询用户列表的服务为例。***Retry***支持***AOP***和程序式两种方式的调用.

#### 程序式的调用方法

和***CircuitBreaker***的调用方式差不多，和熔断器配合使用有两种调用方式，一种是先用重试组件装饰，再用熔断器装饰，这时熔断器的失败需要等重试结束才计算，另一种是先用熔断器装饰，再用重试组件装饰，这时每次调用服务都会记录进熔断器的缓冲环中，需要注意的是，第二种方式需要把***CallNotPermittedException***放进重试组件的白名单中，因为熔断器打开时重试是没有意义的：

```
public class CircuitBreakerServiceImpl {
    
    @Autowired
    private RemoteServiceConnector remoteServiceConnector;
    
    @Autowired
    private CircuitBreakerRegistry circuitBreakerRegistry;
    
    @Autowired
    private RetryRegistry retryRegistry;

    public List<User> circuitBreakerRetryNotAOP(){
        // 通过注册器获取熔断器的实例
        CircuitBreaker circuitBreaker = circuitBreakerRegistry.circuitBreaker("backendA");
        // 通过注册器获取重试组件实例
        Retry retry = retryRegistry.retry("backendA");
        CircuitBreakerUtil.getCircuitBreakerStatus("执行开始前：", circuitBreaker);
        // 先用重试组件包装，再用熔断器包装
        CheckedFunction0<List<User>> checkedSupplier = Retry.decorateCheckedSupplier(retry, remoteServiceConnector::process);
        CheckedFunction0<List<User>> chainedSupplier = CircuitBreaker .decorateCheckedSupplier(circuitBreaker, checkedSupplier);
        // 使用Try.of().recover()调用并进行降级处理
        Try<List<User>> result = Try.of(chainedSupplier).
                recover(CallNotPermittedException.class, throwable -> {
                    log.info("已经被熔断，停止重试");
                    return new ArrayList<>();
                })
                .recover(throwable -> {
                    log.info("重试失败: " + throwable.getLocalizedMessage());
                    return new ArrayList<>();
                });
        RetryUtil.getRetryStatus("执行结束: ", retry);
        CircuitBreakerUtil.getCircuitBreakerStatus("执行结束：", circuitBreaker);
        return result.get();
    }
}
```

#### AOP式的调用方法

首先在连接器方法上使用***@Retry(name="",fallbackMethod="")***注解，其中***name***是要使用的重试器实例的名称，***fallbackMethod***是要使用的降级方法：

```
public RemoteServiceConnector{
    
    @CircuitBreaker(name = "backendA", fallbackMethod = "fallBack")
    @Retry(name = "backendA", fallbackMethod = "fallBack")
    public List<User> process() throws TimeoutException, InterruptedException {
        List<User> users;
        users = remoteServic.process();
        return users;
    }
} 
```

要求和熔断器一致，但是需要注意同时注解重试组件和熔断器的话，是按照第二种方案来的，即每一次请求都会被熔断器记录。

之后直接调用方法：

```
public class CircuitBreakerServiceImpl {
    
    @Autowired
    private RemoteServiceConnector remoteServiceConnector;
    
    @Autowired
    private CircuitBreakerRegistry circuitBreakerRegistry;
    
    @Autowired
    private RetryRegistry retryRegistry;

    public List<User> circuitBreakerRetryAOP() throws TimeoutException, InterruptedException {
        List<User> result = remoteServiceConnector.process();
        RetryUtil.getRetryStatus("执行结束：", retryRegistry.retry("backendA"));
        CircuitBreakerUtil
            .getCircuitBreakerStatus("执行结束：", circuitBreakerRegistry.circuitBreaker("backendA"));
        return result;
    }
}
```

### 使用测试

异常***A***和***B***在***application.yml***文件中设定为都需要重试，因为使用第一种方案，所以不需要将***CallNotPermittedException***设定在重试组件的白名单中，同时为了测试重试过程中的异常是否会被熔断器记录，将异常***A***从熔断器白名单中去除：

```
recordExceptions: # 记录的异常
    - com.example.resilience4j.exceptions.BusinessBException
    - com.example.resilience4j.exceptions.BusinessAException
ignoreExceptions: # 忽略的异常
#   - com.example.resilience4j.exceptions.BusinessAException
# ...
resultPredicate: com.example.resilience4j.predicate.RetryOnResultPredicate
retryExceptions:
    - com.example.resilience4j.exceptions.BusinessBException
    - com.example.resilience4j.exceptions.BusinessAException
    - io.github.resilience4j.circuitbreaker.CallNotPermittedException
ignoreExceptions:
#   - io.github.resilience4j.circuitbreaker.CallNotPermittedException
```

使用另一个远程服务接口的实现，将***num%4==2***的情况返回***null***，测试根据返回结果进行重试的功能：

```
public class RemoteServiceImpl implements RemoteService {

    private static AtomicInteger count = new AtomicInteger(0);

    public List<User> process() {
        int num = count.getAndIncrement();
        log.info("count的值 = " + num);
        if (num % 4 == 1){
            throw new BusinessAException("异常A，需要重试");
        }
        if (num % 4 == 2){
            return null;
        }
        if (num % 4 == 3){
            throw new BusinessBException("异常B，需要重试");
        }
        log.info("服务正常运行，获取用户列表");
        // 模拟数据库的正常查询
        return repository.findAll();
    }
}
```

同时添加一个类自定义哪些返回值需要重试，设定为返回值为空就进行重试，这样***num % 4 == 2***时就可以测试不抛异常，根据返回结果进行重试了：

```
public class RetryOnResultPredicate implements Predicate {

    @Override
    public boolean test(Object o) {
        return o == null ? true : false;
    }
}
```

使用***CircuitBreakerServiceImpl***中的***AOP***或者程序式调用方法进行单元测试，循环调用**10**次：

```
public class CircuitBreakerServiceImplTest{
    
    @Autowired
    private CircuitBreakerServiceImpl circuitService;
    
    @Test
    public void circuitBreakerRetryTest() {
        for (int i=0; i<10; i++){
            // circuitService.circuitBreakerRetryAOP();
            circuitService.circuitBreakerRetryNotAOP();
        }
    }
}
```

看一下运行结果：

```
count的值 = 0
服务正常运行，获取用户列表
执行结束: state= metrics[ failedRetryNum=0, failedNotRetryNum=0, successfulRetryNum=0, successfulNotyRetryNum=1 ]
执行结束：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 1
重试：第1次
count的值 = 2
重试：第2次
count的值 = 3
服务调用失败：2019-07-09T19:06:59.705+08:00[Asia/Shanghai]: Retry 'backendA' recorded a failed retry attempt. Number of retry attempts: '3', Last exception was: 'com.example.resilience4j.exceptions.BusinessBException: 异常B，需要重试'.
重试失败: 异常B，需要重试
执行结束: state= metrics[ failedRetryNum=1, failedNotRetryNum=0, successfulRetryNum=0, successfulNotyRetryNum=1 ]
执行结束：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=2, failedCalls=1, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
```

这部分结果可以看出来，重试最大次数设置为**3**结果其实只重试了**2**次，服务共执行了**3**次，重试**3**次后熔断器只记录了**1**次。而且返回值为***null***时也确实进行重试了。

```
服务正常运行，获取用户列表
执行结束: state= metrics[ failedRetryNum=2, failedNotRetryNum=0, successfulRetryNum=0, successfulNotyRetryNum=3 ]
执行结束：state=OPEN , metrics[ failureRate=40.0, bufferedCalls=5, failedCalls=2, successCalls=3, maxBufferCalls=5, notPermittedCalls=0 ]
已经被熔断，停止重试
执行结束: state= metrics[ failedRetryNum=2, failedNotRetryNum=0, successfulRetryNum=0, successfulNotyRetryNum=3 ]
执行结束：state=OPEN , metrics[ failureRate=40.0, bufferedCalls=5, failedCalls=2, successCalls=3, maxBufferCalls=5, notPermittedCalls=1 ]
```

当熔断之后不会再进行重试。

接下来我修改一下调用服务的实现：

```
public class RemoteServiceImpl implements RemoteService {

    private static AtomicInteger count = new AtomicInteger(0);

    public List<User> process() {
        int num = count.getAndIncrement();
        log.info("count的值 = " + num);
        if (num % 4 == 1){
            throw new BusinessAException("异常A，需要重试");
        }
        if (num % 4 == 3){
            return null;
        }
        if (num % 4 == 2){
            throw new BusinessBException("异常B，需要重试");
        }
        log.info("服务正常运行，获取用户列表");
        // 模拟数据库的正常查询
        return repository.findAll();
    }
}
```

将***num%4==2***变成异常***B***，***num%4==3***变成返回***null***，看一下最后一次重试返回值为***null***属于重试成功还是重试失败。

运行结果如下：

```
count的值 = 0
服务正常运行，获取用户列表
执行结束: state= metrics[ failedRetryNum=0, failedNotRetryNum=0, successfulRetryNum=0, successfulNotyRetryNum=1 ]
执行结束：state=CLOSED , metrics[ failureRate=-1.0, bufferedCalls=1, failedCalls=0, successCalls=1, maxBufferCalls=5, notPermittedCalls=0 ]
count的值 = 1
重试：第1次
count的值 = 2
重试：第2次
count的值 = 3
服务调用成功：2019-07-09T19:17:35.836+08:00[Asia/Shanghai]: Retry 'backendA' recorded a successful retry attempt. Number of retry attempts: '3', Last exception was: 'com.example.resilience4j.exceptions.BusinessBException: 异常B，需要重试'.
```

如上可知如果最后一次重试不抛出异常就算作重试成功，不管结果是否需要继续重试。

## Bulkhead

### 简介

***Resilence4j***的***Bulkhead***提供两种实现，一种是基于信号量的，另一种是基于有等待队列的固定大小的线程池的，由于基于信号量的***Bulkhead***能很好地在多线程和***I/O***模型下工作，所以选择介绍基于信号量的***Bulkhead***的使用。

### 可配置参数

配置参数

默认值

描述

maxConcurrentCalls

25

可允许的最大并发线程数

maxWaitDuration

0

尝试进入饱和舱壁时应阻止线程的最大时间

### 测试前准备

#### pom.xml

不需要引入新的依赖，已经集成在***resilience4j-spring-boot***中了

#### application.yml配置

```
resilience4j:
  bulkhead:
    configs:
      default:
        maxConcurrentCalls: 10
        maxWaitDuration: 1000
    instances:
      backendA:
        baseConfig: default
        maxConcurrentCalls: 3
      backendB:
        baseConfig: default
        maxWaitDuration: 100
```

和***CircuitBreaker***差不多，都是可以通过继承覆盖配置设定实例的。

#### 用于监控Bulkhead状态及事件的工具类

同样为了监控***Bulkhead***组件，写一个工具类：

```
@Log4j2
public class BulkhdadUtil {

    /**
     * @Description: 获取bulkhead的状态
     */
    public static void getBulkheadStatus(String time, Bulkhead bulkhead){
        Bulkhead.Metrics metrics = bulkhead.getMetrics();
        // Returns the number of parallel executions this bulkhead can support at this point in time.
        int availableConcurrentCalls =  metrics.getAvailableConcurrentCalls();
        // Returns the configured max amount of concurrent calls
        int maxAllowedConcurrentCalls = metrics.getMaxAllowedConcurrentCalls();

        log.info(time  + ", metrics[ availableConcurrentCalls=" + availableConcurrentCalls +
                ", maxAllowedConcurrentCalls=" + maxAllowedConcurrentCalls + " ]");
    }

    /**
     * @Description: 监听bulkhead事件
     */
    public static void addBulkheadListener(Bulkhead bulkhead){
        bulkhead.getEventPublisher()
                .onCallFinished(event -> log.info(event.toString()))
                .onCallPermitted(event -> log.info(event.toString()))
                .onCallRejected(event -> log.info(event.toString()));
    }
}
```

### 调用方法

还是以之前查询用户列表的服务为例。***Bulkhead***支持***AOP***和程序式两种方式的调用。

#### 程序式的调用方法

调用方法都类似，装饰方法之后用***Try.of().recover()***来执行：

```
public class BulkheadServiceImpl {

    @Autowired
    private RemoteServiceConnector remoteServiceConnector;

    @Autowired
    private BulkheadRegistry bulkheadRegistry;
    
    public List<User> bulkheadNotAOP(){
        // 通过注册器获得Bulkhead实例
        Bulkhead bulkhead = bulkheadRegistry.bulkhead("backendA");
        BulkhdadUtil.getBulkheadStatus("开始执行前: ", bulkhead);
        // 通过Try.of().recover()调用装饰后的服务
        Try<List<User>> result = Try.of(
            Bulkhead.decorateCheckedSupplier(bulkhead, remoteServiceConnector::process))
            .recover(BulkheadFullException.class, throwable -> {
                log.info("服务失败: " + throwable.getLocalizedMessage());
                return new ArrayList();
            });
        BulkhdadUtil.getBulkheadStatus("执行结束: ", bulkhead);
        return result.get();
    }
}
```

#### AOP式的调用方法

首先在连接器方法上使用***@Bulkhead(name="", fallbackMethod="", type="")***注解，其中***name***是要使用的***Bulkhead***实例的名称，***fallbackMethod***是要使用的降级方法，***type***是选择信号量或线程池的***Bulkhead***：

```
public RemoteServiceConnector{
    
    @Bulkhead(name = "backendA", fallbackMethod = "fallback", type = Bulkhead.Type.SEMAPHORE)
    public List<User> process() throws TimeoutException, InterruptedException {
        List<User> users;
        users = remoteServic.process();
        return users;
    }
    
    private List<User> fallback(BulkheadFullException e){
        log.info("服务失败: " + e.getLocalizedMessage());
        return new ArrayList();
    }
} 
```

如果***Retry***、***CircuitBreaker***、***Bulkhead***同时注解在方法上，默认的顺序是***Retry>CircuitBreaker>Bulkhead***，即先控制并发再熔断最后重试，之后直接调用方法：

```
public class BulkheadServiceImpl {
    
    @Autowired
    private RemoteServiceConnector remoteServiceConnector;
    
    @Autowired
    private BulkheadRegistry bulkheadRegistry;

    public List<User> bulkheadAOP() throws TimeoutException, InterruptedException {
        List<User> result = remoteServiceConnector.process();
        BulkheadUtil.getBulkheadStatus("执行结束：", bulkheadRegistry.retry("backendA"));
        return result;
    }
}
```

### 使用测试

在***application.yml***文件中将***backenA***线程数限制为**1**，便于观察，最大等待时间为***1s***，超过***1s***的会走降级方法：

```
instances:
    backendA:
        baseConfig: default
        maxConcurrentCalls: 1
```

使用另一个远程服务接口的实现，不抛出异常，当做正常服务进行：

```
public class RemoteServiceImpl implements RemoteService {

    private static AtomicInteger count = new AtomicInteger(0);

    public List<User> process() {
        int num = count.getAndIncrement();
        log.info("count的值 = " + num);
        log.info("服务正常运行，获取用户列表");
        // 模拟数据库正常查询
        return repository.findAll();
    }
}
```

用线程池调**5**个线程去请求服务：

```
public class BulkheadServiceImplTest{
    
    @Autowired
    private BulkheadServiceImpl bulkheadService;
    
    @Autowired
    private BulkheadRegistry bulkheadRegistry;
    
    @Test
    public void bulkheadTest() {
        BulkhdadUtil.addBulkheadListener(bulkheadRegistry.bulkhead("backendA"));
        ExecutorService pool = Executors.newCachedThreadPool();
        for (int i=0; i<5; i++){
            pool.submit(() -> {
                // bulkheadService.bulkheadAOP();
                bulkheadService.bulkheadNotAOP();
            });
        }
        pool.shutdown();

        while (!pool.isTerminated());
        }
    }
}
```

看一下运行结果：

```
开始执行前: , metrics[ availableConcurrentCalls=1, maxAllowedConcurrentCalls=1 ]
开始执行前: , metrics[ availableConcurrentCalls=1, maxAllowedConcurrentCalls=1 ]
开始执行前: , metrics[ availableConcurrentCalls=1, maxAllowedConcurrentCalls=1 ]
开始执行前: , metrics[ availableConcurrentCalls=1, maxAllowedConcurrentCalls=1 ]
Bulkhead 'backendA' permitted a call.
count的值 = 0
服务正常运行，获取用户列表
开始执行前: , metrics[ availableConcurrentCalls=0, maxAllowedConcurrentCalls=1 ]
Bulkhead 'backendA' rejected a call.
Bulkhead 'backendA' rejected a call.
Bulkhead 'backendA' rejected a call.
Bulkhead 'backendA' rejected a call.
服务失败: Bulkhead 'backendA' is full and does not permit further calls
执行结束: , metrics[ availableConcurrentCalls=0, maxAllowedConcurrentCalls=1 ]
服务失败: Bulkhead 'backendA' is full and does not permit further calls
执行结束: , metrics[ availableConcurrentCalls=0, maxAllowedConcurrentCalls=1 ]
服务失败: Bulkhead 'backendA' is full and does not permit further calls
执行结束: , metrics[ availableConcurrentCalls=0, maxAllowedConcurrentCalls=1 ]
服务失败: Bulkhead 'backendA' is full and does not permit further calls
执行结束: , metrics[ availableConcurrentCalls=0, maxAllowedConcurrentCalls=1 ]
Bulkhead 'backendA' has finished a call.
执行结束: , metrics[ availableConcurrentCalls=1, maxAllowedConcurrentCalls=1 ]
```

由上可以看出，**5**个请求只有一个进入，其余触发***rejected***事件，然后自动进入降级方法。接下来我们把等待时间稍微加长一些：

```
instances:
    backendA:
        baseConfig: default
        maxConcurrentCalls: 1
        maxWaitDuration: 5000
```

再运行一次：

```
开始执行前: , metrics[ availableConcurrentCalls=1, maxAllowedConcurrentCalls=1 ]
开始执行前: , metrics[ availableConcurrentCalls=1, maxAllowedConcurrentCalls=1 ]
开始执行前: , metrics[ availableConcurrentCalls=1, maxAllowedConcurrentCalls=1 ]
开始执行前: , metrics[ availableConcurrentCalls=1, maxAllowedConcurrentCalls=1 ]
开始执行前: , metrics[ availableConcurrentCalls=1, maxAllowedConcurrentCalls=1 ]
Bulkhead 'backendA' permitted a call.
count的值 = 0
服务正常运行，获取用户列表
Bulkhead 'backendA' permitted a call.
count的值 = 1
Bulkhead 'backendA' has finished a call.
服务正常运行，获取用户列表
执行结束: , metrics[ availableConcurrentCalls=0, maxAllowedConcurrentCalls=1 ]
Bulkhead 'backendA' has finished a call.
执行结束: , metrics[ availableConcurrentCalls=1, maxAllowedConcurrentCalls=1 ]
Bulkhead 'backendA' permitted a call.
```

前面的线程没有马上被拒绝，而是等待了一段时间再执行。

## RateLimiter

### 简介

高频控制是可以限制服务调用频率，***Resilience4j***的***RateLimiter***可以对频率进行纳秒级别的控制，在每一个周期刷新可以调用的次数，还可以设定线程等待权限的时间。

### 可配置参数

配置参数

默认值

描述

timeoutDuration

5\[s\]

线程等待权限的默认等待时间

limitRefreshPeriod

500\[ns\]

权限刷新的时间，每个周期结束后，RateLimiter将会把权限计数设置为limitForPeriod的值

limiteForPeriod

50

一个限制刷新期间的可用权限数

### 测试前准备

#### pom.xml

不需要引入新的依赖，已经集成在***resilience4j-spring-boot***中了

#### application.yml配置

```
resilience4j:
 ratelimiter:
    configs:
      default:
        limitForPeriod: 5
        limitRefreshPeriod: 1s
        timeoutDuration: 5s
    instances:
      backendA:
        baseConfig: default
        limitForPeriod: 1
      backendB:
        baseConfig: default
        timeoutDuration: 0s
```

#### 用于监控RateLimiter状态及事件的工具类

同样为了监控***RateLimiter***组件，写一个工具类：

```
@Log4j2
public class RateLimiterUtil {

    /**
     * @Description: 获取rateLimiter的状态
     */
    public static void getRateLimiterStatus(String time, RateLimiter rateLimiter){
        RateLimiter.Metrics metrics = rateLimiter.getMetrics();
        // Returns the number of availablePermissions in this duration.
        int availablePermissions =  metrics.getAvailablePermissions();
        // Returns the number of WaitingThreads
        int numberOfWaitingThreads = metrics.getNumberOfWaitingThreads();

        log.info(time  + ", metrics[ availablePermissions=" + availablePermissions +
                ", numberOfWaitingThreads=" + numberOfWaitingThreads + " ]");
    }

    /**
     * @Description: 监听rateLimiter事件
     */
    public static void addRateLimiterListener(RateLimiter rateLimiter){
        rateLimiter.getEventPublisher()
                .onSuccess(event -> log.info(event.toString()))
                .onFailure(event -> log.info(event.toString()));
    }
}
```

### 调用方法

还是以之前查询用户列表的服务为例。***RateLimiter***支持***AOP***和程序式两种方式的调用。

#### 程序式的调用方法

调用方法都类似，装饰方法之后用***Try.of().recover()***来执行：

```
public class RateLimiterServiceImpl {

    @Autowired
    private RemoteServiceConnector remoteServiceConnector;

    @Autowired
    private RateLimiterRegistry rateLimiterRegistry;
    
    public List<User> ratelimiterNotAOP(){
        // 通过注册器获得RateLimiter实例
        RateLimiter rateLimiter = rateLimiterRegistry.rateLimiter("backendA");
        RateLimiterUtil.getRateLimiterStatus("开始执行前: ", rateLimiter);
        // 通过Try.of().recover()调用装饰后的服务
        Try<List<User>> result = Try.of(
            Bulkhead.decorateCheckedSupplier(rateLimiter, remoteServiceConnector::process))
            .recover(BulkheadFullException.class, throwable -> {
                log.info("服务失败: " + throwable.getLocalizedMessage());
                return new ArrayList();
            });
        RateLimiterUtil.getRateLimiterStatus("执行结束: ", rateLimiter);
        return result.get();
    }
}
```

#### AOP式的调用方法

首先在连接器方法上使用***@RateLimiter(name="", fallbackMethod="")***注解，其中***name***是要使用的***RateLimiter***实例的名称，***fallbackMethod***是要使用的降级方法：

```
public RemoteServiceConnector{
    
    @RateLimiter(name = "backendA", fallbackMethod = "fallback")
    public List<User> process() throws TimeoutException, InterruptedException {
        List<User> users;
        users = remoteServic.process();
        return users;
    }
    
    private List<User> fallback(BulkheadFullException e){
        log.info("服务失败: " + e.getLocalizedMessage());
        return new ArrayList();
    }
} 
```

如果***Retry***、***CircuitBreaker***、***Bulkhead***、***RateLimiter***同时注解在方法上，默认的顺序是***Retry>CircuitBreaker>RateLimiter>Bulkhead***，即先控制并发再限流然后熔断最后重试

接下来直接调用方法：

```
public class RateLimiterServiceImpl {
    
    @Autowired
    private RemoteServiceConnector remoteServiceConnector;
    
    @Autowired
    private RateLimiterRegistry rateLimiterRegistry;

    public List<User> rateLimiterAOP() throws TimeoutException, InterruptedException {
        List<User> result = remoteServiceConnector.process();
        BulkheadUtil.getBulkheadStatus("执行结束：", rateLimiterRegistry.retry("backendA"));
        return result;
    }
}
```

### 使用测试

在***application.yml***文件中将***backenA***设定为***20s***只能处理**1**个请求，为便于观察，刷新时间设定为***20s***，等待时间设定为***5s***：

```
configs:
      default:
        limitForPeriod: 5
        limitRefreshPeriod: 20s
        timeoutDuration: 5s
    instances:
      backendA:
        baseConfig: default
        limitForPeriod: 1
```

使用另一个远程服务接口的实现，不抛出异常，当做正常服务进行，为了让结果明显一些，让方法***sleep 5***秒：

```
public class RemoteServiceImpl implements RemoteService {

    private static AtomicInteger count = new AtomicInteger(0);

    public List<User> process() throws InterruptedException  {
        int num = count.getAndIncrement();
        log.info("count的值 = " + num);
        Thread.sleep(5000);
        log.info("服务正常运行，获取用户列表");
        // 模拟数据库正常查询
        return repository.findAll();
    }
}
```

用线程池调**5**个线程去请求服务：

```
public class RateLimiterServiceImplTest{
    
    @Autowired
    private RateLimiterServiceImpl rateLimiterService;
    
    @Autowired
    private RateLimiterRegistry rateLimiterRegistry;
    
    @Test
    public void rateLimiterTest() {
        RateLimiterUtil.addRateLimiterListener(rateLimiterRegistry.rateLimiter("backendA"));
        ExecutorService pool = Executors.newCachedThreadPool();
        for (int i=0; i<5; i++){
            pool.submit(() -> {
                // rateLimiterService.rateLimiterAOP();
                rateLimiterService.rateLimiterNotAOP();
            });
        }
        pool.shutdown();

        while (!pool.isTerminated());
        }
    }
}
```

看一下测试结果：

```
开始执行前: , metrics[ availablePermissions=1, numberOfWaitingThreads=0 ]
开始执行前: , metrics[ availablePermissions=1, numberOfWaitingThreads=0 ]
开始执行前: , metrics[ availablePermissions=1, numberOfWaitingThreads=0 ]
开始执行前: , metrics[ availablePermissions=1, numberOfWaitingThreads=0 ]
开始执行前: , metrics[ availablePermissions=0, numberOfWaitingThreads=0 ]
RateLimiterEvent{type=SUCCESSFUL_ACQUIRE, rateLimiterName='backendA', creationTime=2019-07-10T17:06:15.735+08:00[Asia/Shanghai]}
count的值 = 0
RateLimiterEvent{type=FAILED_ACQUIRE, rateLimiterName='backendA', creationTime=2019-07-10T17:06:20.737+08:00[Asia/Shanghai]}
RateLimiterEvent{type=FAILED_ACQUIRE, rateLimiterName='backendA', creationTime=2019-07-10T17:06:20.739+08:00[Asia/Shanghai]}
RateLimiterEvent{type=FAILED_ACQUIRE, rateLimiterName='backendA', creationTime=2019-07-10T17:06:20.740+08:00[Asia/Shanghai]}
服务失败: RateLimiter 'backendA' does not permit further calls
服务失败: RateLimiter 'backendA' does not permit further calls
执行结束: , metrics[ availablePermissions=0, numberOfWaitingThreads=1 ]
执行结束: , metrics[ availablePermissions=0, numberOfWaitingThreads=1 ]
RateLimiterEvent{type=FAILED_ACQUIRE, rateLimiterName='backendA', creationTime=2019-07-10T17:06:20.745+08:00[Asia/Shanghai]}
服务正常运行，获取用户列表
服务失败: RateLimiter 'backendA' does not permit further calls
执行结束: , metrics[ availablePermissions=0, numberOfWaitingThreads=0 ]
服务失败: RateLimiter 'backendA' does not permit further calls
执行结束: , metrics[ availablePermissions=0, numberOfWaitingThreads=0 ]
执行结束: , metrics[ availablePermissions=1, numberOfWaitingThreads=0 ]
```

只有一个服务调用成功，其他都执行失败了。现在我们把刷新时间调成***1s***：

```
configs:
      default:
        limitForPeriod: 5
        limitRefreshPeriod: 1s
        timeoutDuration: 5s
    instances:
      backendA:
        baseConfig: default
        limitForPeriod: 1
```

重新执行，结果如下：

```
开始执行前: , metrics[ availablePermissions=2, numberOfWaitingThreads=0 ]
开始执行前: , metrics[ availablePermissions=2, numberOfWaitingThreads=0 ]
开始执行前: , metrics[ availablePermissions=2, numberOfWaitingThreads=0 ]
开始执行前: , metrics[ availablePermissions=2, numberOfWaitingThreads=0 ]
开始执行前: , metrics[ availablePermissions=2, numberOfWaitingThreads=0 ]
RateLimiterEvent{type=SUCCESSFUL_ACQUIRE, rateLimiterName='backendA', creationTime=2019-07-10T18:25:18.894+08:00[Asia/Shanghai]}
 count的值 = 0
RateLimiterEvent{type=SUCCESSFUL_ACQUIRE, rateLimiterName='backendA', creationTime=2019-07-10T18:25:18.894+08:00[Asia/Shanghai]}
count的值 = 1
RateLimiterEvent{type=SUCCESSFUL_ACQUIRE, rateLimiterName='backendA', creationTime=2019-07-10T18:25:19.706+08:00[Asia/Shanghai]}
count的值 = 2
RateLimiterEvent{type=SUCCESSFUL_ACQUIRE, rateLimiterName='backendA', creationTime=2019-07-10T18:25:19.706+08:00[Asia/Shanghai]}
count的值 = 3
RateLimiterEvent{type=SUCCESSFUL_ACQUIRE, rateLimiterName='backendA', creationTime=2019-07-10T18:25:20.703+08:00[Asia/Shanghai]}
count的值 = 4
服务正常运行，获取用户列表
服务正常运行，获取用户列表
服务正常运行，获取用户列表
服务正常运行，获取用户列表
执行结束: , metrics[ availablePermissions=2, numberOfWaitingThreads=0 ]
执行结束: , metrics[ availablePermissions=2, numberOfWaitingThreads=0 ]
执行结束: , metrics[ availablePermissions=2, numberOfWaitingThreads=0 ]
 执行结束: , metrics[ availablePermissions=2, numberOfWaitingThreads=0 ]
服务正常运行，获取用户列表
执行结束: , metrics[ availablePermissions=2, numberOfWaitingThreads=0 ]
```

可以看出，几个服务都被放入并正常执行了，即使上个服务还没完成，依然可以放入，只与时间有关，而与线程无关。

最后编辑于

：2019.07.29 18:22:07

更多精彩内容，就在简书APP

![](https://upload.jianshu.io/images/js-qrc.png)

"小礼物走一走，来简书关注我"

还没有人赞赏，支持一下

[![  ](https://upload.jianshu.io/users/upload_avatars/17742950/539751e2-afb7-4efc-ac52-41759b0e8545.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/100/h/100/format/webp)](https://www.jianshu.com/u/c609247224ce)

-   序言：七十年代末，一起剥皮案震惊了整个滨河市，随后出现的几起案子，更是在滨河造成了极大的恐慌，老刑警刘岩，带你破解...
    
    [![](https://upload.jianshu.io/users/upload_avatars/15878160/783c64db-45e5-48d7-82e4-95736f50533e.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/48/h/48/format/webp)沈念sama](https://www.jianshu.com/u/dcd395522934)阅读 144,247评论 1赞 305
    
-   序言：滨河连续发生了三起死亡事件，死亡现场离奇诡异，居然都是意外死亡，警方通过查阅死者的电脑和手机，发现死者居然都...
    
-   文/潘晓璐 我一进店门，熙熙楼的掌柜王于贵愁眉苦脸地迎上来，“玉大人，你说我怎么就摊上这事。” “怎么了？”我有些...
    
-   文/不坏的土叔 我叫张陵，是天一观的道长。 经常有香客问我，道长，这世上最难降的妖魔是什么？ 我笑而不...
    
-   正文 为了忘掉前任，我火速办了婚礼，结果婚礼上，老公的妹妹穿的比我还像新娘。我一直安慰自己，他们只是感情好，可当我...
    
    [![](https://upload.jianshu.io/users/upload_avatars/4790772/388e473c-fe2f-40e0-9301-e357ae8f1b41.jpeg?imageMogr2/auto-orient/strip|imageView2/1/w/48/h/48/format/webp)茶点故事](https://www.jianshu.com/u/0f438ff0a55f)阅读 49,160评论 1赞 260
    
-   文/花漫 我一把揭开白布。 她就那样静静地躺着，像睡着了一般。 火红的嫁衣衬着肌肤如雪。 梳的纹丝不乱的头发上，一...
    
-   那天，我揣着相机与录音，去河边找鬼。 笑死，一个胖子当着我的面吹牛，可吹牛的内容都是我干的。 我是一名探鬼主播，决...
    
-   文/苍兰香墨 我猛地睁开眼，长吁一口气：“原来是场噩梦啊……” “哼！你这毒妇竟也来了？” 一声冷哼从身侧响起，我...
    
-   想象着我的养父在大火中拼命挣扎，窒息，最后皮肤化为焦炭。我心中就已经是抑制不住地欢快，这就叫做以其人之道，还治其人...
    
-   序言：老挝万荣一对情侣失踪，失踪者是张志新（化名）和其女友刘颖，没想到半个月后，有当地人在树林里发现了一具尸体，经...
    
-   正文 独居荒郊野岭守林人离奇死亡，尸身上长有42处带血的脓包…… 初始之章·张勋 以下内容为张勋视角 年9月15日...
    
    [![](https://upload.jianshu.io/users/upload_avatars/4790772/388e473c-fe2f-40e0-9301-e357ae8f1b41.jpeg?imageMogr2/auto-orient/strip|imageView2/1/w/48/h/48/format/webp)茶点故事](https://www.jianshu.com/u/0f438ff0a55f)阅读 29,401评论 2赞 217
    
-   正文 我和宋清朗相恋三年，在试婚纱的时候发现自己被绿了。 大学时的朋友给我发了我未婚夫和他白月光在一起吃饭的照片。...
    
    [![](https://upload.jianshu.io/users/upload_avatars/4790772/388e473c-fe2f-40e0-9301-e357ae8f1b41.jpeg?imageMogr2/auto-orient/strip|imageView2/1/w/48/h/48/format/webp)茶点故事](https://www.jianshu.com/u/0f438ff0a55f)阅读 30,747评论 1赞 232
    
-   白月光回国，霸总把我这个替身辞退。还一脸阴沉的警告我。\[不要出现在思思面前， 不然我有一百种方法让你生不如死。\]我...
    
-   序言：一个原本活蹦乱跳的男人离奇死亡，死状恐怖，灵堂内的尸体忽然破棺而出，到底是诈尸还是另有隐情，我是刑警宁泽，带...
    
-   正文 年R本政府宣布，位于F岛的核电站，受9级特大地震影响，放射性物质发生泄漏。R本人自食恶果不足惜，却给世界环境...
    
    [![](https://upload.jianshu.io/users/upload_avatars/4790772/388e473c-fe2f-40e0-9301-e357ae8f1b41.jpeg?imageMogr2/auto-orient/strip|imageView2/1/w/48/h/48/format/webp)茶点故事](https://www.jianshu.com/u/0f438ff0a55f)阅读 31,670评论 3赞 213
    
-   文/蒙蒙 一、第九天 我趴在偏房一处隐蔽的房顶上张望。 院中可真热闹，春花似锦、人声如沸。这庄子的主人今日做“春日...
    
-   文/苍兰香墨 我抬头看了看天上的太阳。三九已至，却和暖如春，着一层夹袄步出监牢的瞬间，已是汗流浃背。 一阵脚步声响...
    
-   我被黑心中介骗来泰国打工， 没想到刚下飞机就差点儿被人妖公主榨干…… 1. 我叫王不留，地道东北人。 一个月前我还...
    
-   正文 我出身青楼，却偏偏与公主长得像，于是被迫代替她去往敌国和亲。 传闻我的和亲对象是个残疾皇子，可洞房花烛夜当晚...
    
    [![](https://upload.jianshu.io/users/upload_avatars/4790772/388e473c-fe2f-40e0-9301-e357ae8f1b41.jpeg?imageMogr2/auto-orient/strip|imageView2/1/w/48/h/48/format/webp)茶点故事](https://www.jianshu.com/u/0f438ff0a55f)阅读 33,819评论 2赞 237
    

### 被以下专题收入，发现更多相似内容
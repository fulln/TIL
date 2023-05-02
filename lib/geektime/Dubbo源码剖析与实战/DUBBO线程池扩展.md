---
dg-publish: true
---

#java #dubbo #极客时间 

##  线程池扩展：如何选择Dubbo线程池？

### DUBBO 线程池原理

Dubbo 采用默认的线程池，也就是 200 个核心线程，来提供服务。


1. 常见线程池结构
![[Pasted image 20230216223514.png]]

拒绝策列，主要包含下面4种
策略一：拒绝添加新任务并抛出异常（AbortPolicy），同时也是默认的拒绝策略。
策略二：让调用方线程执行新任务（CallerRunsPolicy）。
策略三：抛弃新任务（DiscardPolicy）。
策略四：丢弃最早入队的任务然后添加新任务（DiscardOldestPolicy）。

2. dubbo有4种线程池用法。
Dubbo 线程池的创建方式，就是基于刚刚的拥有 7 个参数的线程池构造方法，分别是：

#### FixedThreadPool

```java

///////////////////////////////////////////////////
// org.apache.dubbo.common.threadpool.support.fixed.FixedThreadPool
// 固定线程数量的线程池
///////////////////////////////////////////////////
public class FixedThreadPool implements ThreadPool {

    @Override
    public Executor getExecutor(URL url) {
        // 获取一些参数变量
        String name = url.getParameter("threadname", (String) url.getAttribute("threadname", "Dubbo"));
        int threads = url.getParameter("threads", 200);
        int queues = url.getParameter("queues", 0);
        
        // 调用创建线程池的构造方法
        return new ThreadPoolExecutor(
              // 核心线程数量：threads
              threads, 
              // 最大线程数量：threads
              threads, 
              // 非核心线程空闲时的存活时间等于0
              0, 
              // 非核心线程空闲时的存活时间等于0，单位：毫秒
              TimeUnit.MILLISECONDS,
              // 存放任务的阻塞队列
                      queues == 0 ? new SynchronousQueue<Runnable>() :
                              (queues < 0 ? new LinkedBlockingQueue<Runnable>()
                                      : new LinkedBlockingQueue<Runnable>(queues)),
              // 创建线程的工厂
              new NamedInternalThreadFactory(name, true), 
              // 带有导出线程堆栈的拒绝策略，内部继承了 AbortPolicy 抛异常策略
              new AbortPolicyWithReport(name, url)
        );
    }
}
```
可以看出来3个结论

1. 第一，核心线程数量与最大线程数量是一致的。这说明只有核心线程的存在，没有非核心线程的存在，而且在没有人为干预设置 threads 属性的情况下，默认核心线程数是 200，这也是 Dubbo 默认线程池数量是 200 个的由来。
2. 采用的阻塞队列，是根据队列长度 queues 属性值来确定。长度等于 0 使用同步队列（SynchronousQueue），长度小于 0 使用无界阻塞队列，长度大于 0 使用有界队列。
3. 拒绝策略使用的是默认的抛异常策略。不过，这个拒绝策略是经过框架特殊包装处理的，发现拒绝添加任务时，这个策略有导出线程堆栈的能力，特别适合开发人员分析线程池满时的一些实时状况。

称之为**固定线程数量的线程池（FixedThreadPool）**

#### LimitedThreadPool

```java

///////////////////////////////////////////////////
// org.apache.dubbo.common.threadpool.support.limited.LimitedThreadPool
// 有限制数量的线程池
///////////////////////////////////////////////////
public class LimitedThreadPool implements ThreadPool {

    @Override
    public Executor getExecutor(URL url) {
        // 获取一些参数变量
        String name = url.getParameter("threadname", (String) url.getAttribute("threadname", "Dubbo"));
        int cores = url.getParameter("corethreads", 0);
        int threads = url.getParameter("threads", 200);
        int queues = url.getParameter("queues", 0);
        
        // 调用创建线程池的构造方法
        return new ThreadPoolExecutor(
              // 核心线程数量：cores
              cores, 
              // 最大线程数量：threads
              threads, 
              // 非核心线程空闲时的永久存活
              Long.MAX_VALUE, 
              // 非核心线程空闲时的存活时间，单位：毫秒
              TimeUnit.MILLISECONDS,
              // 存放任务的阻塞队列
                      queues == 0 ? new SynchronousQueue<Runnable>() :
                              (queues < 0 ? new LinkedBlockingQueue<Runnable>()
                                      : new LinkedBlockingQueue<Runnable>(queues)),
              // 创建线程的工厂
              new NamedInternalThreadFactory(name, true), 
              // 带有导出线程堆栈的拒绝策略，内部继承了 AbortPolicy 抛异常策略
              new AbortPolicyWithReport(name, url)
        );
    }
}
```

1. 核心线程数是由一个单独的 corethreads 属性来赋值的，默认值为 0。最大线程数是由 threads 属性来赋值的，默认值为 200。这说明默认情况下没有核心线程，非核心线程数量最大也不能超过 200。
2. 非核心线程的 keepAliveTime 存活时间为 Long 类型的最大值，也就是说永不过期，一旦非核心线程创建出来了，只要不出现什么意外，就会一直存活

**有限制数量的线程池（LimitedThreadPool）。**

- CachedThreadPool
```java

///////////////////////////////////////////////////
// org.apache.dubbo.common.threadpool.support.cached.CachedThreadPool
// 缓存一定数量的线程池
///////////////////////////////////////////////////
public class CachedThreadPool implements ThreadPool {

    @Override
    public Executor getExecutor(URL url) {
        // 获取一些参数变量
        String name = url.getParameter("threadname", (String) url.getAttribute("threadname", "Dubbo"));
        int cores = url.getParameter("corethreads", 0);
        int threads = url.getParameter("threads", Integer.MAX_VALUE);
        int queues = url.getParameter("queues", 0);
        int alive = url.getParameter("alive", 60 * 1000);
        
        // 调用创建线程池的构造方法
        return new ThreadPoolExecutor(
              // 核心线程数量：cores
              cores, 
              // 最大线程数量：threads
              threads, 
              // 非核心线程空闲时的存活时间
              alive, 
              // 非核心线程空闲时的存活时间，单位：毫秒
              TimeUnit.MILLISECONDS,
              // 存放任务的阻塞队列
                      queues == 0 ? new SynchronousQueue<Runnable>() :
                              (queues < 0 ? new LinkedBlockingQueue<Runnable>()
                                      : new LinkedBlockingQueue<Runnable>(queues)),
              // 创建线程的工厂
              new NamedInternalThreadFactory(name, true), 
              // 带有导出线程堆栈的拒绝策略，内部继承了 AbortPolicy 抛异常策略
              new AbortPolicyWithReport(name, url)
        );
    }
}
```

自带销毁非核心线程的线程池

- EagerThreadPool。
```java

///////////////////////////////////////////////////
// org.apache.dubbo.common.threadpool.support.eager.EagerThreadPool
// 渴望数量的线程池
///////////////////////////////////////////////////
public class EagerThreadPool implements ThreadPool {

    @Override
    public Executor getExecutor(URL url) {
        // 获取一些参数变量
        String name = url.getParameter("threadname", (String) url.getAttribute("threadname", "Dubbo"));
        int cores = url.getParameter("corethreads", 0);
        int threads = url.getParameter("threads", Integer.MAX_VALUE);
        int queues = url.getParameter("queues", 0);
        int alive = url.getParameter("alive", 60 * 1000);

        // 初始化队列和线程池
        TaskQueue<Runnable> taskQueue = new TaskQueue<Runnable>(queues <= 0 ? 1 : queues);
        EagerThreadPoolExecutor executor = new EagerThreadPoolExecutor(
                // 核心线程数量：cores
                cores,
                // 最大线程数量：threads
                threads,
                // 非核心线程空闲时的存活时间
                alive,
                // 非核心线程空闲时的存活时间，单位：毫秒
                TimeUnit.MILLISECONDS,
                // 存放任务的阻塞队列
                taskQueue,
                // 创建线程的工厂
                new NamedInternalThreadFactory(name, true),
                // 带有导出线程堆栈的拒绝策略，内部继承了 AbortPolicy 抛异常策略
                new AbortPolicyWithReport(name, url));
        // 将队列和线程池建立联系
        taskQueue.setExecutor(executor);
        return executor;
    }
}
                  ↓
///////////////////////////////////////////////////
// org.apache.dubbo.common.threadpool.support.eager.TaskQueue#offer
// 尝试添加任务至队列
///////////////////////////////////////////////////                  
@Override
public boolean offer(Runnable runnable) {
    // 参数必要性检查，若线程池对象为 null 则抛出异常
    if (executor == null) {
        throw new RejectedExecutionException("The task queue does not have executor!");
    }
    
    // 获取线程池中工作线程 worker 的数量
    int currentPoolThreadSize = executor.getPoolSize();
    // have free worker. put task into queue to let the worker deal with task.
    // 若线程池中活跃的数量小于 worker 的数量，
    // 说明有些 worker 是闲置状态，没有活干
    // 因此把任务添加到队列后，线程就有机会被分派到任务继续干活了
    if (executor.getActiveCount() < currentPoolThreadSize) {
        return super.offer(runnable);
    }
    
    // return false to let executor create new worker.
    // 还能来到这里，说明目前所有的 worker 都在处于工作状态
    // 那么继续看 worker 的数量和最大线程数量想比，若偏小的话
    // 那么就返回 false 表示需要继续创建 worker 来干活
    // 至于为什么返回 false 就能创建 worker 来继续干活，请看下面的 execute 方法
    if (currentPoolThreadSize < executor.getMaximumPoolSize()) {
        return false;
    }
    
    // currentPoolThreadSize >= max
    // 还能来到这里，说明已经达到了最大线程数量了，
    // 那该放队列就放队列，队列放不下的的话，又没有非核心线程了，那就走拒绝策略了
    return super.offer(runnable);
}
                  ↓
///////////////////////////////////////////////////
// java.util.concurrent.ThreadPoolExecutor#execute
// 线程池添加任务的方法
// 解释：currentPoolThreadSize < executor.getMaximumPoolSize() 这行代码
//      为什么返回 false 就能创建 worker 来继续干活
// 原理：在 workQueue.offer(command) 返回 false 后继续走下面的
//      else if (!addWorker(command, false)) 尝试添加 worker 工作线程，
//      添加成功了，那就执行任务，添加不成功了，说明已达到了最大线程数量，走拒绝策略
///////////////////////////////////////////////////  
public void execute(Runnable command) {
    // 若任务 command 对象为 null 的话，是不合法的，直接抛出 NPE 异常
    if (command == null)
        throw new NullPointerException();
    int c = ctl.get();
    
    // 若工作线程的数量小于核心线程的数量的话
    if (workerCountOf(c) < corePoolSize) {
        // 则添加核心线程，addWorker(command, true) 中的 true 表示创建核心线程
        // 添加成功就结束该 execute 方法流程了
        if (addWorker(command, true))
            return;
        c = ctl.get();
    }
    
    // 若还能来到这里，说明工作线程数量已经达到了核心线程的数量了
    // 再来的任务就只能尝试添加至任务阻塞队列了
    // 调用队列的 offer 方法尝试看看能否添加至任务队列
    if (isRunning(c) && workQueue.offer(command)) {
        int recheck = ctl.get();
        // 若添加成功了，但是呢，线程池不处于运行状态，还得将任务移除，
        // 然后执行拒绝策略
        if (! isRunning(recheck) && remove(command))
            reject(command);
        else if (workerCountOf(recheck) == 0)
            addWorker(null, false);
    }
    
    // 还能来到这里，说明线程池处于运行状态，但是尝试添加至队列 offer 失败了
    // 那么就再次尝试调用 addWorker(command, false) 来创建非核心线程来执行任务
    // 尝试添加失败的话，再走拒绝策略
    else if (!addWorker(command, false))
        reject(command);
}
```

特点：

1. 核心线程数是由一个单独的 corethreads 属性来赋值的，默认值为 0。最大线程数是由 threads 属性来赋值的，默认值为 200，非核心线程的存活时间是由 alive 属性来赋值的，基本上都交给了用户自由设置指定。
2. 任务阻塞队列，既不是 SynchronousQueue，也不是 LinkedBlockingQueue，而是重新设计了一款新的阻塞队列 TaskQueue 放到了线程池中。

TaskQueue 亮点在于**重写了 LinkedBlockingQueue 的 offer 方法，只要活跃的工作线程数量小于最大线程数量，就优先创建工作线程来处理任务**。

### 线程池监控

新建一个 MonitorFixedThreadPool 来继承 FixedThreadPool 应该不是什么难事。再拿到线程池对象就比较简单了，在新创建的类中重写 getExecutor 方法，把父类创建的线程池缓存起来。

```java

///////////////////////////////////////////////////
// 自定义监控固定数量的线程池
///////////////////////////////////////////////////
@Slf4j
public class MonitorFixedThreadPool extends FixedThreadPool implements Runnable {

    private static final Set<ThreadPoolExecutor> EXECUTOR_SET = new HashSet<>();
    
    /** <h2>高水位线阈值</h2> **/
    private static final double HIGH_WATER_MARK = 0.85;
    
    // 默认的构造方法，借用该构造方法创建一个带有轮询机制的单线程池
    public MonitorFixedThreadPool() {
        Executors.newSingleThreadScheduledExecutor()
                .scheduleWithFixedDelay(
                        // 当前的 MonitorFixedThreadPool 对象自己
                        this,
                        // 启动后 0 秒执行一次
                        0,
                        // 每间隔 30 秒轮询检测一次
                        30,
                        // 单位：秒
                        TimeUnit.SECONDS
                );
    }
    
    // 重写了父类的 FixedThreadPool 的 getExecutor 方法
    // 然后择机将返回值 executor 存储起来了
    @Override
    public Executor getExecutor(URL url) {
        // 通过 super 直接调用父类的方法，拿到结果
        Executor executor = super.getExecutor(url);
        
        // 针对结果进行缓存处理
        if (executor instanceof ThreadPoolExecutor) {
            EXECUTOR_SET.add((ThreadPoolExecutor) executor);
        }
        return executor;
    }
    
    @Override
    public void run() {
        // 每隔 30 秒，这个 run 方法被触发执行一次    
        for (ThreadPoolExecutor executor : EXECUTOR_SET) {
            // 循环检测每隔线程池是否超越高水位线        
            doCheck(executor);
        }
    }    
    
    // 检测方法
    private void doCheck(ThreadPoolExecutor executor) {
        final int activeCount = executor.getActiveCount();
        int maximumPoolSize = executor.getMaximumPoolSize();
        double percent = activeCount / (maximumPoolSize * 1.0);
        
        // 判断计算出来的值，是否大于高水位线
        if (percent > HIGH_WATER_MARK) {
            log.info("溢出高水位线：activeCount={}, maximumPoolSize={}, percent={}",
                    activeCount, maximumPoolSize, percent);
                    
            // 记录打点，将该信息同步值 Cat 监控平台
            CatUtils.logEvent("线程池溢出高水位线",
                    executor.getClass().getName(),
                    "1", buildCatLogDetails(executor));
        }
    }    
}

///////////////////////////////////////////////////
// 资源目录文件
// 路径为：/META-INF/dubbo/org.apache.dubbo.common.threadpool.ThreadPool
///////////////////////////////////////////////////
monitorfixed=com.hmilyylimh.cloud.threadpool.config.MonitorFixedThreadPool

///////////////////////////////////////////////////
// 修改 Java 代码配置类指定使用该监控线程池
// 或
// dubbo.provider.threadpool=monitorfixed
///////////////////////////////////////////////////
@Bean
public ProtocolConfig protocolConfig(){
    ProtocolConfig protocolConfig = new ProtocolConfig("dubbo", 28260);
    protocolConfig.setThreadpool("monitorfixed");
    return protocolConfig;
}
```

## 地址

此文章为2月day10 学习笔记，内容来源于极客时间《[26｜线程池扩展：如何选择Dubbo线程池？ (geekbang.org)](https://time.geekbang.org/column/article/625394)》，

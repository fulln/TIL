#极客时间 #java 


#### 01 项目性能优化

1. 性能问题分析理论：3S 定理

2. 性能指标：RT、TPS、并发数...

3. 压测监控平台：Docker、InfluxDB、Grafana、Prometheus 和 node_exporter 环境搭建

4. 梯度压测：分析接口性能瓶颈

5. 性能瓶颈剖析

6. 分布式压测：构建百万次请求的压力

7. 服务容器优化：Tomcat、IO 模型、Undertow 等调优

8. 数据库调优：为什么要数据库调优，什么影响数据库性能

9. OpenResty 调优

10. 多级缓存调优

#### 02 JVM 虚拟机

1. JVM 基本常识与整体架构

2. 类加载子系统：加载时机、加载过程

3. 类加载器：Bootstrap ClassLoader、Extension ClassLoader、Application ClassLoader、User ClassLoader

4. JVM 加载机制剖析：一个类的一生

5. 双亲委派与打破双亲委派

6. 自定义类加载器

7. JVM 运行时数据区：堆、虚拟机栈、本地方法栈、方法区、字符串常量池、程序计数器

8. JVM 内存模型变迁

9. 栈帧剖析与栈异常案例

10. 字符串常量池如何存储和查找数据

11. 方法区存储什么，永久代与元空间是什么关系

12. 一个对象的一辈子：对象创建流程与内存分配

13. 对象怎样才会进入老年代？内存担保机制

14. 解剖对象这只小麻雀：对象内存布局，对象头 Header 的 MarkWord 和 KlassPoint

15. 如何定位一个对象

16. GC 基本原理：什么是垃圾、如何找到垃圾，如何清除垃圾，用什么清除垃圾

17. 垃圾收集器剖析：Parallel、Serial、CMS、G1、ZGC

18. Minor GC 、Major GC 和 Full GC

19. JVM 核心参数：标准参数、非标准参数、不稳定参数

20. JVM 常用指令：jps、jstat、jinfo、jhat、jmap

21. JVM 调优工具：VisualVM、GC Easy、PerfMa、MAT

22. GC 日志分析

23. GC 日志分析工具

24. 内存溢出与泄露案例

25. 检测死锁案例

26. 检测死锁案例

27. JVM 调优实战案例：

堆内存和元空间优化

堆栈优化

吞吐量优先策略

响应时间优先策略

G1 全功能垃圾收集策略

#### 03 多线程与并发编程

1. 线程和进程、并发与并行、上下文切换

2. 多线程并发中的线程安全问题

3. 多线程并发的3特性：原子性、可见性、顺序性分析

4. 指令重排序、happens-before规则、

5. JMM 模型深度剖析：JSR-133: Java Memory Model and Thread Specification

6. Synchronized 原理分析：Monitor管程

7. 锁优化&锁升级

8. Volatile 原理与源码分析

9. 多线程在JVM中的实现原理剖析

10. CAS 算法和 ABA 问题

11. 显示锁和 AQS 底层原理分析

12. AQS 共享锁实现原理

13. ReentrantLock 重入锁源码分析

14. ReentrantReadWriteLock 读写锁

15. 并发容器深度剖析

16. CAS 原子操作及相关类

基本数据类型：AtomicInteger、AtomicLong、AtomicBoolean

数组：AtomicIntegerArray、AtomicLongArray、AtomicReferenceArray

引用类型：AtomicReference

17. 并发编程工具掌握：CountDownLatch、Semaphore、CyclicBarrier

18. Future 和 FutureTask

19. 线程池工作原理

20. ThreadLocal 底层原理

#### 04 网络编程

1. 网络通信协议：TCP/IP 协议集

2. TCP/IP 五层模型和 OSI 模型详解

3. TCP 三次握手和四次挥手机制

4. TCP 与 UDP 协议

5. 输入 URL 地址到显示网页经历了哪些过程

6. HTTP1.0 与 HTTP1.1 的区别

7. URI 与 URL 的区别

8. HTTP 与 HTTPS 的区别

9. 同步和异步、阻塞和非阻塞

10. 五种 IO 模型：阻塞 I/O 模型、非阻塞 I/O 模型、多路复用 I/O 模型、信号驱动 I/O 模型、异步 I/O 模型

11. JAVA 网络编程模型：BIO、NIO、AIO

12. NIO 多路复用深入剖析：Selector、Channel 与 SelectionKey

13. NIO 案例 01：客户端与服务器之间通信

14. NIO 案例 02：网络聊天室 V1.0

15. Netty 总体架构设计

16. Netty 线程模型：单线程、多线程与 Netty 线程模型

17. Netty 核心组件：Bootstrap 、EventLoopGroup、Channel 与 ChannelHandlerContext 等

18. Netty 案例 03：客户端与服务器之间通信

19. Netty 案例 04：网络聊天室 V2.0

20. Netty 编解码器

21. RPC 通信原理

22. RPC 的设计架构与思想

23. RPC 架构完整调用流程

24. 案例 05：手写一个 RPC 框架 HeroRPC

25. 案例 06：手写一个 Tomcat

26. 案例 07：600W+ 连接网络应用实战

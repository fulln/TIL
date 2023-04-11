#极客时间 #java 

| 序号 | 内容 |
| --- | --- |
| 01 | 项目性能优化 |
| 1. | 性能问题分析理论：3S 定理 |
| 2. | 性能指标：RT、TPS、并发数... |
| 3. | 压测监控平台：Docker、InfluxDB、Grafana、Prometheus 和 node_exporter 环境搭建 |
| 4. | 梯度压测：分析接口性能瓶颈 |
| 5. | 性能瓶颈剖析 |
| 6. | 分布式压测：构建百万次请求的压力 |
| 7. | 服务容器优化：Tomcat、IO 模型、Undertow 等调优 |
| 8. | 数据库调优：为什么要数据库调优，什么影响数据库性能 |
| 9. | OpenResty 调优 |
| 10. | 多级缓存调优 |
| 02 | JVM |
| 1.|[[jvmKnowns]] | 
| 03 | 多线程与并发编程 |
| 1. | 线程和进程、并发与并行、上下文切换 |
| 2. | 多线程并发中的线程安全问题 |
| 3. | 多线程并发的3特性：原子性、可见性、顺序性分析 |
| 4. | 指令重排序、happens-before规则、 |
| 5. | JMM 模型深度剖析：JSR-133: Java Memory Model and Thread Specification |
| 6. | Synchronized 原理分析：Monitor管程 |
| 7. | 锁优化&锁升级 |
| 8. | Volatile 原理与源码分析 |
| 9. | 多线程在JVM中的实现原理剖析 |
| 10. | CAS 算法和 ABA 问题 |
| 11. | 显示锁和 AQS 底层原理分析 |
| 12. | AQS 共享锁实现原理 |
| 13. | ReentrantLock 重入锁源码分析 |
| 14. | ReentrantReadWriteLock 读写锁 |
| 15. | 并发容器深度剖析 |
| 16. | CAS 原子操作及相关类<br>基本数据类型：AtomicInteger、AtomicLong、AtomicBoolean<br>数组：AtomicIntegerArray、AtomicLongArray、AtomicReferenceArray<br>引用类型：AtomicReference |
| 17. | 并发编程工具掌握：CountDownLatch、Semaphore、CyclicBarrier |
| 18. | Future 和 FutureTask |
| 19. | 线程池工作原理 |
| 20. | ThreadLocal 底层原理 |
| 04 | 网络编程 |
| 1. | 网络通信协议：TCP/IP 协议集 |
| 2. | TCP/IP 五层模型和 OSI 模型详解 |
| 3. | TCP 三次握手和四次挥手机制 |
| 4. | TCP 与 UDP 协议 |
| 5. | 输入 URL 地址到显示网页经历了哪些过程 |
| 6. | HTTP1.0 与 HTTP1.1 的区别 |
| 7. | URI 与 URL 的区别 |
| 8. | HTTP 与 HTTPS 的区别 |
| 9. | 同步和异步、阻塞和非阻塞 |
| 10. | 五种 IO 模型：阻塞 I/O 模型、非阻塞 I/O 模型、多路复用 I/O 模型、信号驱动 I/O 模型、异步 I/O 模型 |
| 11. | JAVA 网络编程模型：BIO、NIO、AIO |
| 12. | NIO 多路复用深入剖析：Selector、
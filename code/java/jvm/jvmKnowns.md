## JVM 虚拟机

### 1. JVM 基本常识与整体架构
![[Pasted image 20230127174345.png]]

### 2. 类加载子系统:加载过程和加载时机
1. [[code/java/jvm/JvmLoadSubSystem#加载过程]]
2. [[code/java/jvm/JvmLoadSubSystem#加载时机]]

### 3.  类加载器：

[[code/java/jvm/classLoader#类加载器]]

### 4. JVM 加载机制剖析：
[[code/java/jvm/JvmLoadSubSystem#类的生命周期]]

### 5. 双亲委派与打破双亲委派
1. [[code/java/jvm/classLoader#双亲委派模型]]
2. [[code/java/jvm/classLoader#破坏双亲委派模型]]

### 6. 自定义类加载器
例子： tomcat

### 7. JVM 运行时数据区
堆、虚拟机栈、本地方法栈、方法区、字符串常量池、程序计数器

### 8. [[code/java/jvm/栈帧剖析]]与栈异常案例

### 9.[[code/java/jvm/字符串常量池]]如何存储和查找数据


### 10. 方法区存储什么，永久代与元空间是什么关系

10. 一个对象的一辈子：对象创建流程与内存分配

11. 对象怎样才会进入老年代？内存担保机制

12. 解剖对象这只小麻雀：对象内存布局，对象头 Header 的 MarkWord 和 KlassPoint

13. 如何定位一个对象

14. GC 基本原理：什么是垃圾、如何找到垃圾，如何清除垃圾，用什么清除垃圾

15. 垃圾收集器剖析：Parallel、Serial、CMS、G1、ZGC

16. Minor GC 、Major GC 和 Full GC

17. JVM 核心参数：标准参数、非标准参数、不稳定参数

18. JVM 常用指令：jps、jstat、jinfo、jhat、jmap

19. JVM 调优工具：VisualVM、GC Easy、PerfMa、MAT

20. GC 日志分析

21. GC 日志分析工具

22. 内存溢出与泄露案例

23. 检测死锁案例

24. 检测死锁案例

25. JVM 调优实战案例：

26. 堆内存和元空间优化

27. 堆栈优化

28. 吞吐量优先策略

29. 响应时间优先策略

30. G1 全功能垃圾收集策略
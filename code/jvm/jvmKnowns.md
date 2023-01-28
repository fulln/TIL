## JVM 虚拟机

### 1. JVM 基本常识与整体架构
^543e16
![[Pasted image 20230127174345.png]]

### 2. 类加载子系统:加载过程和加载时机

![[JvmLoadSubarray#加载过程概括]]
![[JvmLoadSubarray#加载时机]]

### 3.  类加载器：
Bootstrap ClassLoader、Extension ClassLoader、Application ClassLoader、User ClassLoader

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

28. 堆内存和元空间优化

29. 堆栈优化

30. 吞吐量优先策略

31. 响应时间优先策略

32. G1 全功能垃圾收集策略
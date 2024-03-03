---
createTime: 2024-03-03 19:55
tags:
  - java
  - javabasic
  - object
---
## 面向对象
 - 封装
 - 继承
 - 多态
 - 抽象

## javaObjects

###  object在内存中的布局
- markword
	- 32位机器上保持的就是32bit，64位机器则是64bit
	- 结构组成
		 - 2bit的锁状态位(无锁状态、偏向锁状态、轻量级锁状态和重量级锁状态)
		 - 4bit的gc分代年龄
		 - object的hashcode
		 - 1bit的偏向锁标志(如果为true的话, 还会记录持有锁的线程id)
  - class指针
  - 对象实例
  - 对齐填充（64byte,看机器位数就补充对应位数

#### 偏向锁

并不是在所有情况下都能提高程序运行效率，只有在竞争不激烈的情况下，偏向锁才能发挥优势。如果竞争激烈，频繁的锁撤销和重偏向操作反而会增加额外的开销。因此，偏向锁的启用需要根据实际情况进行调整，可以通过JVM参数`-XX:+UseBiasedLocking和-XX:BiasedLockingStartupDelay`进行控制。

- XX:+UseBiasedLocking：这个参数用于启用或禁用偏向锁。如果设置为-XX:+UseBiasedLocking，则启用偏向锁；如果设置为-XX:-UseBiasedLocking，则禁用偏向锁。默认情况下，这个参数是启用的。 

- XX:BiasedLockingStartupDelay：这个参数用于设置启动偏向锁的延迟时间（单位为秒）。这是因为在程序启动初期，可能会有大量的竞争，此时偏向锁可能不会带来太大的性能提升，反而会因为撤销偏向锁而带来额外的开销。因此，可以通过这个参数设置一个延迟时间，让偏向锁在程序运行一段时间后再启动。默认情况下，这个参数的值为0，即偏向锁立即启动。 
###  equals的实现

  - 自反性：对于任何非空引用 x, x.equals(Object) 将返回 true;
  - 对称性：对于任何引用 x 和 y，当且仅当 y.equals(x)返回 true 时，x.equals(y)返回 true;
  - 传递性：对于任何引用 x、y 和 z，如果x.equals(y) 返回true 并且 y.equals(z)也返回true，那么 x.equals(z) 也应该返回 true;
  - 一致性：如果 x 和 y 引用的对象没有改变，那么 x.equals(y)的重复调用应该返回同一结果；
### java对对象的引用分类

  - 1.强引用
	- 只要引用存在，垃圾回收器永远不会回收
  - 2.软引用
	- 非必须引用，内存溢出之前进行回收，可以通过以下代码实现
  - 3.弱引用
	- 第二次垃圾回收时回收
  - 4.虚引用
	- 虚引用 垃圾回收时回收，无法通过引用取到对象值
## ThreadLocal 解析

### 简介

此类提供线程局部变量。 这些变量不同于它们的普通对应变量，因为每个访问一个（通过其get或set方法）的线程都有自己的、独立初始化的变量副本

> This class provides thread-local variables. These variables differ from their normal counterparts in that each thread that accesses one (via its get or set method) has its own, independently initialized copy of the variable. 

### 类关系

#### 成员变量

```java
/**
 在ThreadLocalMaps中, 用该值来校验 key的hash值 
 */
private final int threadLocalHashCode
/**
  要给出的下一个hashCode ,原子递增,从0开始
 */
private static AtomicInteger nextHashCode =
        new AtomicInteger();
/**
 连续生产的hashcode差异,将顺序生产的线程id转成最优分布的乘法hash值,用于2次方的表
 
 */
private static final int HASH_INCREMENT = 0x61c88647;

```

##### HASH_INCREMENT 为啥是1640531527

hash_increment为十六进制`0x61c88647` 也就是十进制的1640531527,

* 当容量为2的指数值时,所有填充的值hash值最均匀



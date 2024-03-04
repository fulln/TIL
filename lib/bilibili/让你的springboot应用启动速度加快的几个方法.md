---
dg-publish: true
---

## 视频地址

[让你的springboot应用启动速度快到飞起的几个方法！_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Ed4y1X7p7/?spm_id_from=333.337.search-card.all.click&vd_source=1690412baac5d9ecc946844006611737)


## 首先观测应用慢在哪里

1. 观测工具

`async-profile` 工具

## 怎么优化

### 1. 减少业务初始化

启动的时候会包含大量业务逻辑的初始化，如redis，mysql，es等中间件的连接， 业务的数据的初始化。 主要方向是减少业务不必要依赖， 没有必要启动就初始化的业务，能异步就异步初始化

### 2. 延迟初始化

spring-boot 自带 lazy-init 属性，设置为true就表示所有bean的延迟加载，一定程度上提高启动速度，但是初次访问会有过慢的问题

### 3. spring-context-indexer

```xml
<dependency>
	<groupId>org.springframework</groupId>
	<artifactId>spring-context-indexer</artifactId>
	<optional>true</optional>
</dependency>
```

解决类扫描的时候，避免类扫描过多导致扫描速度过慢的问题，在启动类上加上`@Indexed` 注解，在程序编译打包后，会生成 `META-INF/spring-components`文件，当执行`CompomentScan`扫描类时，会读取index文件，提高扫描速度。

### 4. 关闭jmx
spring-boot 2.2之前默认`spring.jmx.enable=false`
如果无需监控，则可以手动关闭

### 5. 关闭分层编译和关闭字节验证

可以手动关闭字节验证，jdk自带c1和c2编译器，手动指定使用C1 编译器，提高启动速度。 但尽量不在生产使用

### 6.  Jar index

通过[[code/java/jvm/JvmLoadSubSystem]]加载jar包，找到对应文件加载， 然后验证，准备，解析，初始化.
`JAR INDEX` 就是用来解决在加载类的时候，遍历jar性能的问题。

#### 使用过程

1. 在A,B,C 3个jar包查找class文件，如果能通过类型前缀`com/A` 立刻推断在哪个jar包，就可以避免jar遍历的过程。

#### 问题

对于现在应用而言，jar index 难应用
1. 通过jar -i 生成的索引文件是基于 `META-INF/MANIFEST.MF` 中的class-path来的，大部分项目不会涉及，所以索引文件生成需要手动处理
2. 只支持URLClassloader，需要自定义类加载逻辑

### 7. APP CDS （application  class data sharding）

主要用于启动加速和节省内存，在jdk1.5引入。 jdk8后支持APPClassloader 和自定义classloader，类在加载过程中伴随[[code/java/jvm/JvmLoadSubSystem#解析(Resolution)]],[[code/java/jvm/JvmLoadSubSystem#验证(Verification)]]等过程，CDS就是将这个过程产生的数据结构存储到归档文件，在下次运行时重复使用，这个归档文件就是Shared Archive ，以jsa文件为后缀，在使用过程中，就是将jsa文件映射到内存中，让对象头的类型指针指向该地址。

APP CDS 只会在包含所有class文件的fat-jar生效，对于spring-boot的嵌套jar结构无法生效。需要用maven-shade 插件创建shade jar

### 8. heap archive
jdk9加载，jdk12 正式使用，heap archive是在类初始化的时候，通过内存映射初始化一些static字段。避免调用类初始化器。提前拿到初始化好的类，提高启动速度。

### 9. AOT 编译

类加载过程的优化，当真正创建对象实例，执行方法的时候，由于可能没有被JIT编译，在解释模式下执行速度非常慢，所以有AOT编译的方式。

AOT指的是程序执行之前的编译行为，作用相当于是预热，提前编译为机器码，减少解释时间。






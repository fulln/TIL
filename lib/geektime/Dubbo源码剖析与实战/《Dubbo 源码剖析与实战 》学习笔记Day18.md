---
dg-publish: true
---

#java #dubbo #极客时间 

## 课程内容

### dubbo spi

#### SPI怎么来的

![[Pasted image 20230202231659.png]]


在工程中，凡是想二次改造开源，不但要考虑开发人员驾驭底层框架的抽象封装能力，还得考虑后续的维护和迭代成本。

代码中定义了一个应用启动成功的监听器接口（ApplicationStartedListener），接着 app-web 自定义一个预加载 Dubbo 资源监听器（PreloadDubboResourcesListener）来实现该接口。

在插件应用成功启动的时刻，会寻找 ApplicationStartedListener 接口的所有实现类，并将所有实现类全部执行一遍，这样，插件既提供了一种口子的规范约束，又能满足业务诉求在应用成功启动时刻做一些事情。

##### JDKSPI

第一块，将接口传入到 ServiceLoader.load 方法后，得到了一个内部类的迭代器。
第二块，通过调用迭代器的 hasNext 方法，去读取“/META-INF/services/ 接口类路径”这个资源文件内容，并逐行解析出所有实现类的类路径。
第三块，将所有实现类的类路径通过“Class.forName”反射方式进行实例化对象。

当我们使用 ServiceLoader 的 load 方法执行多次时，会不断创建新的实例对象。

###### JDK SPI 的问题

问题一，使用 load 方法频率高，容易影响 IO 吞吐和内存消耗。
问题二，使用 load 方法想要获取指定实现类，需要自己进行遍历并编写各种比较代码。

结论一，增加缓存，来降低磁盘 IO 访问以及减少对象的生成。
结论二，使用 Map 的 hash 查找，来提升检索指定实现类的性能。

###### DUBBO SPI

Dubbo 设计出了一个 ExtensionLoader 类，实现了 SPI 思想

第一，定义一个 IDemoSpi 接口，并在该接口上添加 @SPI 注解。
第二，定义一个 CustomSpi 实现类来实现该接口，然后通过 ExtensionLoader 的 getExtension 方法传入指定别名来获取具体的实现类。
最后，在“/META-INF/services/com.hmilyylimh.cloud.dubbo.spi.IDemoSpi”这个资源文件中，添加实现类的类路径，并为类路径取一个别名（customSpi）。

## 课程地址
[ 14｜SPI 机制：Dubbo的SPI比JDK的SPI好在哪里？]([14｜SPI 机制：Dubbo的SPI比JDK的SPI好在哪里？ (geekbang.org)](https://time.geekbang.org/column/article/620900))
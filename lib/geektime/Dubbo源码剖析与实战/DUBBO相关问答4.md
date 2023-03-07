#java #dubbo #极客时间 

##  大厂高频面试：底层的源码逻辑知多少

### 使用 Javassist 编译的有哪些关键要素环节？

- 首先，设计一个代码模板。
- 然后，使用 Javassist 的相关 API，通过 ClassPool.makeClass 得到一个操控类的 CtClass 对象，然后针对 CtClass 进行 addField 添加字段、addMethod 添加方法、addConstructor 添加构造方法等等。
- 最后，调用 CtClass.toClass 方法并编译得到一个类信息，有了类信息，就可以实例化对象处理业务逻辑了。

### 使用 ASM 编译有哪些基本步骤？

- 通过插件获取模板对应字节码
- 使用 Asm 的相关 API 依次将字节码指令翻译为 Asm 对应的语法，比如创建 ClassWriter 相当于创建了一个类，继续调用  ClassWriter.visitMethod 方法相当于创建了一个方法
- 调用 ClassWriter.toByteArray 得到字节码的字节数组，交给 JVM 虚拟机得出一个 Class 类信息。
- 交给 JVM 虚拟机得出一个 Class 类信息。

### Dubbo 是怎么完成实例注入与切面拦截的

1. 当extensionloader的getExtension被调用的时候，初始化对应对象，判断取值缓存还是直接获取对象
2. 创建对象后，包装过程包括前置初始化前置处理（postProcessBeforeInitialization）、注入扩展点（injectExtension）、初始化后置处理（postProcessAfterInitialization）三个阶段
3. 根据@Wrapper注解，添加所有包装类
4. 成员变量通过setter方法从容器中获取
5. 生成对应扩展点对象

### 服务发布的流程是怎样的？

1. 配置
	1. 扫描对应含有@DubboService的bean定义，全部注册到serviceBean中
2. 导出
	1. 本地导出 -> 存到本地内存
	2. 暴露协议的远端导出 -> 通过netty绑定暴露其协议
3. 注册
	1. 通过zookeeper的curator客户端写到zk中


### 服务订阅的流程是怎样的？

1. 通过 @DubboReference 注解来标识需要订阅哪些接口的服务，并使用这些服务进行调用。在源码跟踪上，可以通过该注解一路探索出背后的核心类 ReferenceConfig。
2. 紧接着，在 ReferenceConfig 的 get 方法会先后进行本地引用与远程引用的两大主干流程。
3. 然后，在本地引用环节中使用的 invoker 对象是从 InjvmProtocol 中 exporterMap 获取到的。而在远程引用环节中，创建 invoker 的核心逻辑是在 RegistryProtocol 的 doCreateInvoker 方法中完成的。
4. 最后，在这段 doCreateInvoker 逻辑中，还进行了消费者注册和接口订阅逻辑，订阅逻辑的本质就是启动环节从注册中心拉取一遍接口的所有提供方信息，然后为这些接口添加监听操作，以便在后续的环节中，提供方有任何变化，消费方这边也能通过监听策略，及时感知到提供方节点的变化。

![[Pasted image 20230223230009.png]]


### 消费方调用流程是怎样的？

[[DUBBO消费流程#消费方的调用流程]]

### Dubbo 的协议帧格式？


定长报文头+变长报文体

0xdabb -> 请求类型 & 序列化方式 -> dubbo响应码 -> 请求id ->报文长 






## 地址

此文章为2月day17 学习笔记，内容来源于极客时间《[加餐｜大厂高频面试：底层的源码逻辑知多少？ (geekbang.org)](https://time.geekbang.org/column/article/625429)》
## JDK15视频发布会及新特性

> B站视频地址:<a>https://www.bilibili.com/video/BV1Va4y1s7Qu?t=2884</a> 直接从25分钟看起

### 文本块

文本块（text block）是多行字符串字面量，可以用代码表示，而不必处理大多数转义符号和笨重的连接操作

```java
//例子1
String html = "<html>\n" +
		" <body>\n"+
		"	<p>Hello world.</p>\n"+
		"</body>\n"+
		"</html>\n"; 

// 在jdk 13之后可以用这么表示
String html = """
		<html>
		 <body>
			<p>Hello world.</p>
		 </body>
		</html>
	      """
```

从而可以直接将文本原封不动的剪切并粘贴到编译器中。文本块使用相同的转义序列集，与之前的使用双引号表示字符串的边界不同， 它使用三个双引号作为定界符，中间可以写多行字符串，
但是这转变就留下一个难题，通常想要将文本块和代码使用缩进对齐，但是不希望将这种对齐展示在字符串中，于是采用启发式方法判断哪个缩进是字符串的一部分，而哪个是用来保持文本块和代码对齐的不重要的缩进。
该算法也会在每行最后的非空白字符的右侧隐式添加换行符，jdk15中添加使用`\` 来去掉换行，添加 `\s`来保留空格

### ZGC 和 Shenandoah 转正

在jdk15中，zgc 不再是实验特性，使用ZGC的时候不需要再使用-xx:+UnlockedExperimetalVMOptions开启ZGC，ZGC被设计为在10ms内完成垃圾回收,即时在很大的内存中也是一样（不超过4TB）

### 重新实现DatagramSocket API

DatagramScoket 旧实现可以追溯到JDk1.0，包含java 和c的代码,很难维护，MulticastSocket不支持IPV6，而且还有并发问题。

### Sealed Class 预览版本

如果类和结构被Sealed修饰，那么对它们的继承or实现就受到了限制，java中子类可以继承父类的方法，然而子类的继承关系并不仅仅是为了复用代码，有的时候也是为了对领域中的各个模型进行建模，限制子类集可以简化建模，现有是使用final修饰类，那么这个类就不可以被继承，或者改变类或者构造方法的修饰符，使得类作用范围在package内。然而不能满足出现的额限定子类继承这种形式，目前要使用 Sealed 需要添加jvm参数

```java
//例子2
package com.example

// 这里Shape 没有实现接口和继承其他类
public abstract sealed class Shape
permits Circle,Square,Rectangle
{...}
//permits 子句指定类允许继承sealed class的类

```

sealed Class 对允许继承它的子类施加三种约束
    - Sealed class 和其子类必须属于同一模块或都在一个没有被命名的模块的相同package中
    - 每个被允许的子类都必须直接继承Sealed class
    - Sealed class 的每个子类都必须选择一个修饰符来描述如何延续超类（sealed class）对继承的限制	 
         - 被final修饰
	 - 被sealed修饰
	 - 被non-sealed修饰，任何类都可以继承它          

现在可以使用`java.lang.Class#isSealed`确定一个Class接口是不是密封的，如果是，可以使用`java.lang.Class#permittedSubclasses`获取到允许继承它的类

### instanceof 类型匹配

我们能以更简洁安全的方式表示对从对象中提取出的组件进行条件判断

```java
//例子3
if(obj instanceof String){
	String s = (String)obj
	//...
}

```
在上面我们必须要做三件事情

- 检测obj的类型是否是String
- 定义s
- 将obj强转为String类型，并赋值给s

而现在我们可以写成下面这样

```java
if (obj instanceof String s){
//...
}
```
使用类型匹配将代码缩减成一行，完成之前的三件事情，s只有在 obj是string类型的时候才会强转并赋值给s，并且s的作用域仅仅在if 分支中

### Records 预览

当我们视图使用一个简单的聚合类final字段的类的时候，Record省去类我们必须要创建的一些样板方法,如hash和equals ，tosting等

```java

//例子4
record Point(int x,int y){}

```
local records ，可以将record类型的数据作为中间值用于生产和消费逻辑，可以通过在一个方法中内嵌一个静态的record帮助类or 在靠近操作变量的代码方法内声明一个record

```java
//例子5
List<Merchant> findToMerchants(List<Merchant> merchants,int month){
 	//local record
	record MerchantSales(Merchant merchant,double sales){}
	
	return merchants.stream()
		.map(merchant ->new MerchantSales(merchant,computeSales(merchant,month)))
		.sorted((m1,m2) -> Double.compare(m2.sales(),m1.sales()))
		.map(MerchantSales::merchant)
		.collect(toList())
}
```

### hidden class

许多基于jvm构建的语言实现都依赖于动态类的生成，比如，javac 在编译的时候不会将lambda表达式转换为一个专用的class文件，而是在运行时，根据需要动态生成字节码，并实例化一个类，语言实现者通常都希望动态生成的类在逻辑上成为静态生成类的实现中的一部分。动态生成的类最好是不可被发现的，另外动态生成的类只会被用几次，因此将他们保留在静态生成的类的生命周期中，可能会增加不必要的内存占用量，而当前标准的API不能区分字节码是动态生成还是静态，因此动态生成的类可能比我们想象中更容易被发现，或者生命周期比需要的时间长，通过 hidden class 提高类基于jvm构建的所有语言动态生成类的效率。 

### foregin-memory Access API 二次孵化

外部内存使用，完工后会为访问外存的java程序提供一个有效的替代方案，大多数开发都是使用buffer 来使用java NIO 还有一些错误的想法就是通过buffer访问外存，这个api旨在提供一个性能接近但是更为安全的方案（目前未完工）

### 禁用偏向锁

不推荐使用所有与偏向锁相关的命令行选项，偏向锁是Hotspot虚拟机中使用的一种优化技术，以此来减少没有竞争时使用锁的开销，偏向锁的性能曾比常规锁性能好，但是在现代处理器上执行原子指令的成本已经降低，而偏向锁需要大量复杂代码支持，阻碍了同步子系统的重要设计变更，所以jdk15默认禁用偏向锁，可以用命令行选项打开


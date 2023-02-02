#java #jvm #javabasic 

## 加载过程

### 加载过程概括
1. [加载](#加载(loading)).选择类加载器根据字节流创建对应类的过程
2. [链接](#链接).将创建成的类合并至 Java 虚拟机中，使之能够执行的过程
3. 初始化. 在声明时直接赋值，也可以在静态代码块中对其赋值。只有当初始化完成之后，类才正式成为可执行的状态。 

### 加载(loading)

#### 加载流程

1. 通过类的全限定名称获取类的2进制流(_这个步骤是放在jvm之外执行_)

>主要来源有:	 
>1.从zip包中获取
>2.运行时生成(动态代理)
>3.网络中获取
>4.其他文件生成
>...

2. 将字节流代表的静态存储结构放到方法区中
3. 内存中生成一个class对象,作为这个类的访问入口

#### 类加载器 
负责动态加载Java类到Java虚拟机的内存空间中,任意一个类,**必须由加载它的类加载器和它本身一起确立在jvm中的唯一性**,每一个类加载器都有独立的类名称空间,比较2个类相等只有在这个2个类都是同一个类加载器加载下才有意义

##### 双亲委派模型

jvm角度看 只存在2种不同的加载器
- 启动类加载器(_这个是由c++实现的_)
- 其他类的类加载器(_全在虚拟机之外,并继承ClassLoader_)

3层类加载器
- 启动类加载器(BootstrapClassLoader)
- 扩展类加载器(Extension Class Loader)
- 应用程序类加载器(Application Class Loader) _加载用户类路径上的所有类库,是默认的类加载器_

双亲委派模型要求除了顶层的启动类加载器,其他类加载器,都应该有自己的父类加载器( 这里的父子关系不是以继承实现,而是用组合关系复用父加载器的代码)

###### 双亲委派下加载过程

如果一个类加载器收到加载请求,会先去派给父类执行,每一个加载器都是一样,只有当父类反馈无法完成加载请求的时候,子加载器才会去尝试完成加载

##### 破坏双亲委派模型

1. 有基础类型又要调用回子类的代码.
	1. JDNI代码由启动类加载,但是需要调用其他厂商实现并部署的SPI代码
	2. 通过线程上下文加载器去加载SPI代码
2. 通过类加载器实现热部署,OSGI使用更复杂的网状结构加载
3. JDK修改旧代码时,新增findClass的接口

#### 加载相关点

- 对于非数组加载,用户可以自定义加载器进行类加载(权限很大)
- 数组加载的是jvm直接再内存中创建的
		1.数组的组件类型如果是引用类型的话还是需要用加载器加载
		2.如果不是引用类型的话,会把数组标为与引导类加载器关联
		3.可达性与组件类型保持一致,非引用类型都是public

### 链接

#### 验证(Verification)

验证是确保class中的信息符合jvm规范,不会危害到jvm,在jvm中验证工作占比相当大

##### 验证的阶段

1. 文件格式验证,看是否符合class结构
2. 元数据验证,是否有父类,是否不规则的重载等
3. 字节码验证,判断字节码是否正常跳转,_JDK6之后用stackMaptable属性表用**类型检查**代替**类型推断**从而节约很多时间_
4. 符号引用验证,是否能通过全限定名找到对应类

验证阶段是很重要但不是必须执行的阶段,可以通过设置`-Xverify:none` 跳过验证,缩短启动时间

#### 准备(Preparation)
该阶段就是为类中定义的变量(静态变量)分配内存,并设置初始值,**注意这里的初始值通常指数据类型的0值,不过如果该字段是常量字段,则会被初始化为指定的值**

#### 解析(Resolution)
解析就是将常量池内的符号引用代替为直接引用的过程


## 加载时机
1. 当虚拟机启动时，初始化用户指定的主类；
2. 当遇到用以新建目标类实例的 new 指令时，初始化 new 指令的目标类；
3. 当遇到调用静态方法的指令时，初始化该静态方法所在的类；
4. 当遇到访问静态字段的指令时，初始化该静态字段所在的类；
5. 子类的初始化会触发父类的初始化；
6. 如果一个接口定义了 default 方法，那么直接实现或者间接实现该接口的类的初始化，会触发该接口的初始化；
7. 使用反射 API 对某个类进行反射调用时，初始化这个类；
8. 当初次调用 MethodHandle 实例时，初始化该 MethodHandle 指向的方法所在的类。

## 模块化系统中改进

### 模块化加载的异同
1. 保留了3层类加载器和双亲委派机制,但是将扩展类加载器替换成了平台类加载器(PlatformClassloader)
2. 平台类加载器和应用程序类加载器都不在派生自URLClassloader,jdk9之后 .如果由程序依赖这种关系会导致程序崩溃

### 模块化加载的过程
		在委派给父类加载器之前,先判断该类是否归属到某个模块中,如果可以,优先委派给那个模块的加载器进行加载

解析(Resolution)
	就是将常量池内的符号引用代替为直接引用的过程
	除去 invokedynamic之外.可以对第一次解析的结果进行缓存(从而避免了重复解析的过程)
		无论解析多少次,都需要保证在同一个实体类中,一个符号引用已经被解析成功,后续的所有次解析都能成功.保持连续性,哪怕这个请求的符号已经正确加载到了虚拟机内存,
		invokedynamic指令的目的本来就是用于动态语言支持
			指必须等到程序运行到当前指令的时候解析动作才能进行
	针对符号类型引用进行解析
		类
		接口
		方法类型
		字段
			解析字段所属的类,并返回这个类or接口 C
				1,本身就包含了字段,直接返回字段引用
				2.如果实现了接口,会去接口中从下往上搜索接口和它的父类找这字段
				3. 如果不是Object,会按照继承关系从父类找对应字段
					实际上,接口和父类都有这个字段定义就会拒绝编译
				4.找不到就抛出异常
		方法
			如果类方法的引用类型从常量表找出来是个接口的方法,就报异常
			其他过程和类差不多
			会将该类的方法表也初始化完毕
		接口方法
			接口可以在多个父类中查找对应的简单名称方法
		方法句柄
		调用限定符

初始化(Initialization)
	严格规定只有6种情况必须立即对类初始化
		1.遇到new getstatic,putstatic,invokestatic 这4条指令字节码,如果类没有初始化,必须进行初始化阶段(被final修饰,已经在编译期间放入常量池中的静态字段除外)
		2.使用reflect包方法对类进行反射的时候,如果没有初始化过,则需要触发初始化
		3,类初始化的时候 如果父类没有初始话,则先触发父类的初始化
		4.虚拟机启动时,需要指定一个main类,虚拟机会先初始化这个类
		5.JDK7的动态语言支持时,4种方法句柄(REF_getStatic,REF_putStatic,REF_invokeStatic,REF_newInvokeSpecial)
		6. JDK8的 接口有default方法,需要将接口初始化
	其他的都是被动引用  不会被初始化
		java相对安全的原因
			封装了对数组元素访问的方法而不是直接移动指针,数组越界直接异常,避免了非法内存访问
	对于接口的初始化
		接口中是不能使用static
		与类初始化只有第三点不同
			并不要求父类全部初始化再初始化子类
	初始化就是执行类构造方法<clinit>的过程
		<clinit> 由编译器自动收集的所有类变量的赋值和静态代码块中的语句合并而成
			静态代码块只能访问到定义在静态语句块前的变量,之后的变量可以在静态语句块赋值,不能访问
		同一个加载器下,一个类型只会被初始化一次
		同时只有1个线程去执行类的<clinit>

使用(Using)
	类加载与子系统执行
		tomcat
			common
				类库可以被所有web公用
			server
				类库可被Tomcat使用,对web不可见
			shared
				对web公用,对tomcat不可见
			/WEB-INF/
				每个web单独使用
			多个类加载器
				common类加载器
				catalina类加载器(server)
				shared类加载器
		OSGI
			网形类加载关系(破坏了双亲委派机制)

卸载(unloading)

java模块化系统
	区别
		保留了3层类加载器和双亲委派机制,但是将扩展类加载器替换成了平台类加载器(PlatformClassloader)
		平台类加载器和应用程序类加载器都不在派生自URLClassloader
			jdk9之后 .如果由程序依赖这种关系会导致程序崩溃
	过程
		在委派给父类加载器之前,先判断该类是否归属到某个模块中,如果可以,优先委派给那个模块的加载器进行加载
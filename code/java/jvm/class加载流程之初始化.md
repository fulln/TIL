---
dg-publish: true
---
### 初始化

#### 对类的初始化

严格规定只有6种情况必须立即对类初始化

1. 遇到new getstatic,putstatic,invokestatic 这4条指令字节码,如果类没有初始化,必须进行初始化阶段(被final修饰,已经在编译期间放入常量池中的静态字段除外)
2. 使用reflect包方法对类进行反射的时候,如果没有初始化过,则需要触发初始化
3. 类初始化的时候 如果父类没有初始话,则先触发父类的初始化
4. 虚拟机启动时,需要指定一个main类,虚拟机会先初始化这个类
5. JDK7的动态语言支持时,4种方法句柄(REF_getStatic,REF_putStatic,REF_invokeStatic,REF_newInvokeSpecial)
6. JDK8的 接口有default方法,需要将接口初始化

其他被动引用不会被初始化

##### java相对安全的原因

1. 封装了对数组元素访问的方法而不是直接移动指针
2. 数组越界直接异常,避免了非法内存访问

#### 对接口的初始化

1. 接口中是不能使用static
2. 与类初始化只有第三点不同，并不要求父类全部初始化再初始化子类

#### 初始化对应过程

初始化就是执行类构造方法<clinit>的过程 
1. <clinit> 由编译器自动收集的所有类变量的赋值和静态代码块中的语句合并而成
2. 静态代码块只能访问到定义在静态语句块前的变量,之后的变量可以在静态语句块赋值,不能访问
3. 同一个加载器下,一个类型只会被初始化一次
4. 同时只有1个线程去执行类的<clinit>
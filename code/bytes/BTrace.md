#java #字节码增强 #BTrace

## 通过BTrace进行分析

BTrace 能动态的修改程序行为,是基于java虚拟机的Instrument开发的.阿里的Arthas 也是通过Instrument实现了与BTrace类似的功能

下面是一段demo

```java
/* BTrace Script Template */
import com.sun.btrace.annotations.*;
import static com.sun.btrace.BTraceUtils.*;

@BTrace
public class TracingScript {
	/* put your code here */
    @OnMethod(clazz="com.fulln.common.controller.BTraceTest",method="add",location=@Location(Kind.RETURN))
public static void fun(@Self com.fulln.common.controller.BTraceTest instance,int a,int b ,@Return int result)
{
println("调用堆栈:");
jstack();
println(strcat("方法参数A:",str(a)));
println(strcat("方法参数B:",str(b)));
println(strcat("方法结果",str(result)));
        
}
}
```

在远程的环境下无法连接到远程debug的情况下,可以用BTrace加入原本不存在的代码,idea

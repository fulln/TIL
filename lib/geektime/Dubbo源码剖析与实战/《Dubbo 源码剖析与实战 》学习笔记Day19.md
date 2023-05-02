---
dg-publish: true
---

#java #dubbo #极客时间 

## 课程内容

### dubbo wrapper

Dubbo 中的一种动态生成的代理类。

#### JDK 和CGLIB未满足dubbo需求

##### JDK代理

dubbo 中需要的泛化调用

1. 接口类名
2. 接口方法名
3. 接口参数方法名
4. 业务请求参数

需要分发调用不同的入口服务，这里就可通过反射机制来精确定位哪个服务哪个方法需要调用

代码优化这里， 根据反射把遍历方法的地方改成，根据入参调用各种接口服务方法的能力，但是耗
时很严重

##### CGLIB 代理

使用了第三方库，不方便做2开，难以自主修改。有 Cglib 思想的方案更好，并且还可以在此思想上，利用最简单的代码，定制适合自己框架的代理类


#### 自定义实现

自定义代理类

```java

///////////////////////////////////////////////////
// 代码模板
///////////////////////////////////////////////////
public class $DemoFacadeCustomInvoker extends CustomInvoker {
    @Override
    public Object invokeMethod(Object instance, String mtdName, Class<?>[] types, Object[] args) throws NoSuchMethodException {
        // 这里就是进行简单的 if 代码判断
        if ("sayHello".equals(mtdName)) {
            return ((DemoFacade) instance).sayHello(String.valueOf(args[0]));
        }
        if ("say".equals(mtdName)) {
            return ((DemoFacade) instance).say();
        }
        throw new NoSuchMethodException("Method [" + mtdName + "] not found.");
    }
}
```

生成的代码主要有三个步骤。
- 按照代码模板的样子，使用 Java 代码动态生成出来一份代码字符串。
- 将生成的代码字符串保存到磁盘中。
- 根据磁盘文件路径将文件编译为 class 文件，然后利用 URLClassLoader 加载至内存变成 Class 对象，最后反射创建对象并且实例化对象。

#### dubbo wrapper 原理

```JAVA

// org.apache.dubbo.rpc.proxy.javassist.JavassistProxyFactory#getInvoker
// 创建一个 Invoker 的包装类
@Override
public <T> Invoker<T> getInvoker(T proxy, Class<T> type, URL url) {
    // 这里就是生成 Wrapper 代理对象的核心一行代码
    final Wrapper wrapper = Wrapper.getWrapper(proxy.getClass().getName().indexOf('$') < 0 ? proxy.getClass() : type);
    // 包装一个 Invoker 对象
    return new AbstractProxyInvoker<T>(proxy, type, url) {
        @Override
        protected Object doInvoke(T proxy, String methodName,
                                  Class<?>[] parameterTypes,
                                  Object[] arguments) throws Throwable {
            // 使用 wrapper 代理对象调用自己的 invokeMethod 方法
            // 以此来避免反射调用引起的性能开销
            // 通过强转来实现统一方法调用
            return wrapper.invokeMethod(proxy, methodName, parameterTypes, arguments);
        }
    };
}
```

生成代理类的流程总结起来有 3 点。

- 以源对象的类属性为维度，与生成的代理类建立缓存映射关系，避免频繁创建代理类影响性能。
- 生成了一个继承 Wrapper 的动态类，并且暴露了一个公有 invokeMethod 方法来调用源对象的方法。
- 在 invokeMethod 方法中，通过生成的 if…else 逻辑代码来识别调用源对象的不同方法。

#### dubbo wrapper 的弊端

Wrapper 机制，对于搭建高性能的底层调用框架还是非常高效的，而且开辟了一条直接通过 Java 代码生成代理类的简便途径，为框架的未来各种定制扩展，提供了非常灵活的自主控制权。但不适合大众化，因为 Wrapper 机制定制化程度高，对维护人员会有较高的开发门槛要求。


## 课程地址

 [15｜Wrapper机制：Wrapper是怎么降低调用开销的？]([15｜Wrapper机制：Wrapper是怎么降低调用开销的？ (geekbang.org)](https://time.geekbang.org/column/article/620918))
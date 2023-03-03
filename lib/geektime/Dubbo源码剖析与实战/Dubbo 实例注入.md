#java #dubbo #极客时间 

## 课程内容

###  dubbo 对象创建

包含[[《Dubbo 源码剖析与实战 》学习笔记Day21#Dubbo Adaptive]]的相关内容。自适应扩展点是实例创建的一个特殊实现

#### 创建的流程

1. `createAdaptiveExtension` 
2. `createExtension`

```JAVA

///////////////////////////////////////////////////
// 根据指定扩展点名称去创建扩展点实例对象
///////////////////////////////////////////////////
// org.apache.dubbo.common.extension.ExtensionLoader#createExtension
@SuppressWarnings("unchecked")
private T createExtension(String name, boolean wrap) {
    // getExtensionClasses 为当前 SPI 接口的所有实现类的类信息集合
    // 通过指定的扩展点名称 name 来获取与之对应的实现类类信息
    Class<?> clazz = getExtensionClasses().get(name);
    // 若找不到对应的扩展点，或者当初加载时扩展点有重复名称的话
    // 这里都会抛出查找异常
    if (clazz == null || unacceptableExceptions.contains(name)) {
        throw findException(name);
    }
    
    try {
        // extensionInstances 为当前 SPI 接口已经经过实例化的实例对象集合
        // 然后通过指定的扩展点名称看看有没有与之对应的已经曾经创建好的实例对象
        T instance = (T) extensionInstances.get(clazz);
        // 若找不到，说明没有缓存，从而则说明该扩展点名称也是首次使用
        if (instance == null) {
            // 通过并发 Map 的 putIfAbsent 方法以线程安全的形式，
            // 来保证该实现类只会创建一个实例对象，实例对象是反射方式创建出来的
            extensionInstances.putIfAbsent(clazz, createExtensionInstance(clazz));
            
            // putIfAbsent 执行完，只要不报错，那就说明指定扩展点名称的实现类创建成功了
            // 那么就继续把刚刚创建出来的实例对象再次 get 出来
            // 此时的 instance 应该称之为原始未经过初始化的裸体对象
            instance = (T) extensionInstances.get(clazz);
            
            // 初始化前置处理，即将原始的对象进行前置包装等处理
            instance = postProcessBeforeInitialization(instance, name);
            
            // 扩展点注入
            injectExtension(instance);
            
            // 初始化后置处理，即将已初始化实例化注入的对象进行后置包装等处理
            instance = postProcessAfterInitialization(instance, name);
        }
        
        // wrap 是否需要进行装饰器包装
        if (wrap) {
            List<Class<?>> wrapperClassesList = new ArrayList<>();
            // 看看是否有装饰器包装类，即实现类中单一参数的构造方法是不是 SPI 接口
            if (cachedWrapperClasses != null) {
                // 如果有装饰器包装类，那么就将该 SPI 接口中所有包装实现类进行排序
                wrapperClassesList.addAll(cachedWrapperClasses);
                wrapperClassesList.sort(WrapperComparator.COMPARATOR);
                Collections.reverse(wrapperClassesList);
            }
            if (CollectionUtils.isNotEmpty(wrapperClassesList)) {
                // 循环装饰器包装类，进行层层套娃包装
                for (Class<?> wrapperClass : wrapperClassesList) {
                    // 装饰器类上是否 Wrapper 注解
                    Wrapper wrapper = wrapperClass.getAnnotation(Wrapper.class);
                    
                    // 1. 没有 wrapper 注解，需要进行包装
                    // 2. wrapper 中的 matches 字段值为空没有内容，需要进行包装
                    // 3. wrapper 中的 matches 字段值不为空并包含入参 name 值，并且 mismatches 字段值不包含 name 值，需要进行包装
                    // 4. 其他情况，可能就是瞎写乱配，导致无法进行包装之类的
                    boolean match = (wrapper == null) ||
                        ((ArrayUtils.isEmpty(wrapper.matches()) || ArrayUtils.contains(wrapper.matches(), name)) &&
                            !ArrayUtils.contains(wrapper.mismatches(), name));
                    
                    // 如果匹配成功，则进行包装
                    if (match) {
                        // 针对包装的类再次进行实例注入
                        instance = injectExtension((T) wrapperClass.getConstructor(type).newInstance(instance));
                        // 针对包装类，同样进行后置处理
                        instance = postProcessAfterInitialization(instance, name);
                    }
                }
            }
        }
        
        // Warning: After an instance of Lifecycle is wrapped by cachedWrapperClasses, it may not still be Lifecycle instance, this application may not invoke the lifecycle.initialize hook.
        initExtension(instance);
        return instance;
    } catch (Throwable t) {
        throw new IllegalStateException("Extension instance (name: " + name + ", class: " +
            type + ") couldn't be instantiated: " + t.getMessage(), t);
    }
}
```

1. 每个扩展点对应一个class类信息 ->对应实例对象 -> 以线程安全的形式保存到缓存中。
2. 刚反射创建出来的扩展点对象，都会经历前置初始化前置处理（postProcessBeforeInitialization）、注入扩展点（injectExtension）、初始化后置处理（postProcessAfterInitialization）三个阶段，经过三段处理的对象，我们暂且称为“原始对象”。
3. 据传入的 wrap 变量，决定是否需要将原始对象再次进行包裹处理 
	1. 无 @Wrapper 注解，则需要包装。
	2. 有 @Wrapper 注解，但是注解中的 matches 字段值为空，则需要包装。
	3. 有 @Wrapper 注解，但是注解中的 matches 字段值包含入参的扩展点名称，并且 mismatches 字段值不包含入参的扩展点名称，则需要包装。

#### 拓展对象的3个处理阶段

1. 初始化前置处理
2. 扩展点后置处理
	1. 初始化前置处理
	2. 初始化后置处理

循环调用每个后置处理器的 postProcessBeforeInitialization 方法，把每一次循环的返参结果放到下一次循环的入参中去。

```JAVA

///////////////////////////////////////////////////
// 初始化前置处理方法
///////////////////////////////////////////////////
// org.apache.dubbo.common.extension.ExtensionLoader#postProcessBeforeInitialization
private T postProcessBeforeInitialization(T instance, String name) throws Exception {
    // 先看看当前框架中有没有设置过后置处理器，有就循环处理一把
    if (extensionPostProcessors != null) {
        // 循环所有的后置处理器，依次调用初始化前置方法
        // 循环体中都会使用经过方法处理后的对象继续下一个循环处理，有点套娃的性质
        for (ExtensionPostProcessor processor : extensionPostProcessors) {
            instance = (T) processor.postProcessBeforeInitialization(instance, name);
        }
    }
    // 最终返回层层套娃之后的对象
    return instance;
}
                  ↓
///////////////////////////////////////////////////
// 扩展点后置处理器，包含两个方法，
// postProcessBeforeInitialization：初始化前置处理
// postProcessAfterInitialization：初始化后置处理
///////////////////////////////////////////////////
// org.apache.dubbo.common.extension.ExtensionPostProcessor
public interface ExtensionPostProcessor {
    // 初始化前置处理
    default Object postProcessBeforeInitialization(Object instance, String name) throws Exception {
        return instance;
    }
    // 初始化后置处理
    default Object postProcessAfterInitialization(Object instance, String name) throws Exception {
        return instance;
    }
}
```

3. 注入扩展点`injectExtension`

```JAVA

///////////////////////////////////////////////////
// 注入扩展点的方法
///////////////////////////////////////////////////
// org.apache.dubbo.common.extension.ExtensionLoader#injectExtension
private T injectExtension(T instance) {
    if (injector == null) {
        return instance;
    }
    try {
        // 拿到实例对象的所有方法集合，然后进行循环处理
        for (Method method : instance.getClass().getMethods()) {
            // 判断方法是否是 set 方法，有 3 个条件：
            // 1. 方法必须是 public 公有修饰属性
            // 2. 方法名称必须以 set 三个字母开头
            // 3. 方法的入参个数必须是 1 个
            // 如果这 3 个条件都不满足的话，那就直接 continue 不做任何处理
            if (!isSetter(method)) {
                continue;
            }
            // 如果发现方法上有 @DisableInject 注解的话，则也不做任何处理
            if (method.isAnnotationPresent(DisableInject.class)) {
                continue;
            }
            // 获取方法参数中第 0 个参数的类型
            // （注意：前面通过 isSetter 已经明确方法的入参只能有 1 个）
            Class<?> pt = method.getParameterTypes()[0];
            // 如果参数类型是基本类型的话，那么也不做任何处理了
            if (ReflectUtils.isPrimitives(pt)) {
                continue;
            }
            // 接下来，能走到这里来，则说明都是需要处理的方法
            try {
                // 获取方法的属性，什么叫属性呢？
                // 比如方法名称为 setVersion 的话，那么就会返回 version 内容
                // 比如方法名称小于 3 个字符的话，那么就返回空字符串
                String property = getSetterProperty(method);
                // 然后根据【参数类型】+【扩展点名称】直接从容器中找到对应的实例对象
                // 所以可以反映出，通过 set 方法就能直接从容器中找到对应的实例并赋值上
                Object object = injector.getInstance(pt, property);
                // 将拿到的实例对象通过反射方式赋值到该 method 方法中的成员变量
                if (object != null) {
                    method.invoke(instance, object);
                }
            } catch (Exception e) {
                logger.error("Failed to inject via method " + method.getName()
                    + " of interface " + type.getName() + ": " + e.getMessage(), e);
            }
        }
    } catch (Exception e) {
        logger.error(e.getMessage(), e);
    }
    return instance;
}
                  ↓
///////////////////////////////////////////////////
// Object object = injector.getInstance(pt, property); 方法的实现逻辑
///////////////////////////////////////////////////
// org.apache.dubbo.common.extension.inject.AdaptiveExtensionInjector#getInstance
@Override
public <T> T getInstance(Class<T> type, String name) {
    // 循环所有的扩展点注入器，每个注入器可以粗浅的理解为一个容器
    // 那也就是说，循环每种容器，看看能不能根据类型加名字，找到对应的实例对象
    for (ExtensionInjector injector : injectors) {
        // 循环每种容器，从容器中根据类型加名字获取实例对象
        T extension = injector.getInstance(type, name);
        // 一旦获取到了的话，那就直接返回即可，不用再循环其他容器了
        if (extension != null) {
            return extension;
        }
    }
    return null;
}
                  ↓
///////////////////////////////////////////////////
// 寻找 injectors 变量被赋值的方法，
// 看到初始化 initialize 的话，想都不用想了，肯定在某个初始化环境被调用的
///////////////////////////////////////////////////
// org.apache.dubbo.common.extension.inject.AdaptiveExtensionInjector#initialize
@Override
public void initialize() throws IllegalStateException {
    // 获取【扩展点注入器】的加载器
    ExtensionLoader<ExtensionInjector> loader = extensionAccessor.getExtensionLoader(ExtensionInjector.class);
    List<ExtensionInjector> list = new ArrayList<ExtensionInjector>();
    // 从加载器中拿出所有的可被使用的注册器实现类
    for (String name : loader.getSupportedExtensions()) {
        list.add(loader.getExtension(name));
    }
    // 然后通过不可变集合包装起来，意味着不允许别人对注册器实现类进行任何修改
    injectors = Collections.unmodifiableList(list);
}
```


**注入的关键点，使用 setter 方法就能直接从容器中找到对应的实例，完成实例注入。**

创建扩展点对象的时候，不但会通过 setter 方法进行实例注入，而且还会通过包装类层层包裹，就像这样。

![[Pasted image 20230206232611.png]]


实现类可以设置 @Wrapper 注解，注解中的 order 属性值越小则越先执行，mismatches 属性值包含入参给定的扩展点名称时，那么该扩展点的方法不会触发执行

#### dubbo 实例注入反思

Spring 存在实例注入，Dubbo 也存在实例注入，它们针对实例进行注入的思想是相通的。都是框架拿到对象时，发现里面有很多字段值是空的，或者有很多设置属性的方法没有被调用，框架就需要将对象里面的字段值赋值。


Spring 支持三种方式注入，字段属性注入、setter 方法注入、构造方法注入。Dubbo 的注入方式只有 _setter 方法注入和构造方法注入这 2 种_，并且 Dubbo 的构造方法注入还有局限性，_构造方法的入参个数只能是一个，且入参类型必须为当前实现类对应的 SPI 接口类型_。





## 课程地址

此文章为2月day1 学习笔记，内容来源于极客时间《[Dubbo源码与实战]([18｜实例注入：实例注入机制居然可以如此简单？ (geekbang.org)](https://time.geekbang.org/column/article/620943))》，推荐该课程
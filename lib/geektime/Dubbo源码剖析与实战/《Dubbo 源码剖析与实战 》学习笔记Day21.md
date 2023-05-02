---
dg-publish: true
---

#java #dubbo #极客时间 

## 课程内容

### Dubbo Adaptive

在加载并解析 SPI 文件的逻辑中，有一段专门针对 Adaptive 注解进行处理的代码；在 Dubbo 内置的被 @SPI 注解标识的接口中，好多方法上都有一个 @Adaptive 注解。

#### 自适应扩展点

`ExtensionLoader 的 getAdaptiveExtension`

主要执行的Adapter 方法

```JAVA

// org.apache.dubbo.common.extension.ExtensionLoader#getAdaptiveExtensionClass
// 创建自适应扩展点方法
private T createAdaptiveExtension() {
    try {
        // 这一行从 newInstance 这个关键字便知道这行代码就是创建扩展点的核心代码
        T instance = (T) getAdaptiveExtensionClass().newInstance();
        
        // 这里针对创建出来的实例对象做的一些类似 Spring 的前置后置的方式处理
        instance = postProcessBeforeInitialization(instance, null);
        instance = injectExtension(instance);
        instance = postProcessAfterInitialization(instance, null);
        initExtension(instance);
        return instance;
    } catch (Exception e) {
        throw new IllegalStateException("Can't create adaptive extension " + type + ", cause: " + e.getMessage(), e);
    }
}
                  ↓
// 获取自适应扩展点的类对象
private Class<?> getAdaptiveExtensionClass() {
    // 获取当前扩展点（Cluster）的加载器（ExtensionLoader）中的所有扩展点
    getExtensionClasses();
    // 如果缓存的自适应扩展点不为空的话，就提前返回
    // 这里也间接的说明了一点，每个扩展点（Cluster）只有一个自适应扩展点对象
    if (cachedAdaptiveClass != null) {
        return cachedAdaptiveClass;
    }
    // 这里便是创建自适应扩展点类对象的逻辑，我们需要直接进入没有缓存时的创建逻辑
    return cachedAdaptiveClass = createAdaptiveExtensionClass();
}
                  ↓
// 创建自适应扩展点类对象                  
private Class<?> createAdaptiveExtensionClass() {
    // Adaptive Classes' ClassLoader should be the same with Real SPI interface classes' ClassLoader
    ClassLoader classLoader = type.getClassLoader();
    try {
        if (NativeUtils.isNative()) {
            return classLoader.loadClass(type.getName() + "$Adaptive");
        }
    } catch (Throwable ignore) {
    }
    // 看见这行关键代码，发现使用了一个叫做扩展点源码生成器的类
    // 看意思，就是调用 generate 方法生成一段 Java 编写的源代码
    String code = new AdaptiveClassCodeGenerator(type, cachedDefaultName).generate();
    // 紧接着把源代码传入了 Compiler 接口的扩展点
    // 这个 Compiler 接口不就是我们上一讲思考题刚学过的知识点么
    org.apache.dubbo.common.compiler.Compiler compiler = extensionDirector.getExtensionLoader(
        org.apache.dubbo.common.compiler.Compiler.class).getAdaptiveExtension();
    // 通过调用 compile 方法，也就大致明白了，就是通过源代码生成一个类对象而已
    return compiler.compile(type, code, classLoader);
	}
```

主要流程：

- 在 Dubbo 框架里，自适应扩展点是通过双检索（DCL）以线程安全的形式创建出来的。
- 创建自适应扩展点时，每个接口有且仅有一个自适应扩展点。
- 自适应扩展点的创建，是通过生成了一段 Java 的源代码，然后使用 Compiler 接口编译生成了一个类对象，这说明自适应扩展点是动态生成的。

**CLuster 接口中的 join 方法被 @Adaptive 注解标识了，但是另外 2 个 getCluster 方法没有被 @Adaptive 标识。**

#### 自适应扩展参数

- 自适应扩展点对象的类名很特殊，是由接口名 +$Adaptive 构成的。
- SPI 接口中，标识了 @Adaptive 注解的方法，到时候在自适应扩展点对象中都会有对应的一套动态代码逻辑。
- 自适应扩展点对象中那些有代理逻辑的方法，代码流程大致是先从 url 获取到指定的扩展点名称，没有指定则使用 SPI 接口默认设置的扩展点名称，总之继续根据扩展点名称，再次获取对应的实现类来触发方法的调用。


ExtensionLoader 的 getAdaptiveExtension 方法，其实返回的是一个自适应的代理对象，代理对象会从 URL 里面获取扩展点名称，来走指定的实现类逻辑。而 SPI 接口的方法上，如果有 @Adaptive 注解，那么这个方法会被代理，代理的逻辑会出现在自适应代理对象中。

#### 加载 SPI 资源文件

##### “SPI 机制”中 loadDirectory

```java

// org.apache.dubbo.common.extension.ExtensionLoader#loadDirectory(java.util.Map<java.lang.String,java.lang.Class<?>>, org.apache.dubbo.common.extension.LoadingStrategy, java.lang.String)
// 加载某一指定目录下的 SPI 文件目录
private void loadDirectory(Map<String, Class<?>> extensionClasses, LoadingStrategy strategy, String type) {
    loadDirectory(extensionClasses, strategy.directory(), type, strategy.preferExtensionClassLoader(),
        strategy.overridden(), strategy.includedPackages(), strategy.excludedPackages(), strategy.onlyExtensionClassLoaderPackages());
    String oldType = type.replace("org.apache", "com.alibaba");
    loadDirectory(extensionClasses, strategy.directory(), oldType, strategy.preferExtensionClassLoader(),
        strategy.overridden(), strategy.includedPackagesInCompatibleType(), strategy.excludedPackages(), strategy.onlyExtensionClassLoaderPackages());
}
                  ↓
// loadDirectory 方法的重载，还是加载某一指定目录下的 SPI 文件目录
private void loadDirectory(Map<String, Class<?>> extensionClasses, String dir, String type,
                           boolean extensionLoaderClassLoaderFirst, boolean overridden, String[] includedPackages,
                           String[] excludedPackages, String[] onlyExtensionClassLoaderPackages) {
    String fileName = dir + type;
    try {
        // 这里省略了其他部分代码
        
        Map<ClassLoader, Set<java.net.URL>> resources = ClassLoaderResourceLoader.loadResources(fileName, classLoadersToLoad);
        // 这里通过 SPI 文件目录找到了多个文件
        // 于是循环每个文件进行挨个读取内容
        resources.forEach(((classLoader, urls) -> {
            loadFromClass(extensionClasses, overridden, urls, classLoader, includedPackages, excludedPackages, onlyExtensionClassLoaderPackages);
        }));
    } catch (Throwable t) {
        logger.error("Exception occurred when loading extension class (interface: " +
            type + ", description file: " + fileName + ").", t);
    }
}
                  ↓
// 循环 SPI 文件的多个路径，然后想办法读取资源路径的内容                  
private void loadFromClass(Map<String, Class<?>> extensionClasses, boolean overridden, Set<java.net.URL> urls, ClassLoader classLoader,
                           String[] includedPackages, String[] excludedPackages, String[] onlyExtensionClassLoaderPackages) {
    if (CollectionUtils.isNotEmpty(urls)) {
        for (java.net.URL url : urls) {
            loadResource(extensionClasses, classLoader, url, overridden, includedPackages, excludedPackages, onlyExtensionClassLoaderPackages);
        }
    }
}
                  ↓
// 读取单个资源文件的内容，通过 BufferedReader 进行逐行读取解析内容
private void loadResource(Map<String, Class<?>> extensionClasses, ClassLoader classLoader,
                          java.net.URL resourceURL, boolean overridden, String[] includedPackages, String[] excludedPackages, String[] onlyExtensionClassLoaderPackages) {
    try {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(resourceURL.openStream(), StandardCharsets.UTF_8))) {
            String line;
            String clazz;
            while ((line = reader.readLine()) != null) {
               // 这里省略了其他部分代码
                if (StringUtils.isNotEmpty(clazz) && !isExcluded(clazz, excludedPackages) && isIncluded(clazz, includedPackages)
                    && !isExcludedByClassLoader(clazz, classLoader, onlyExtensionClassLoaderPackages)) {
                    loadClass(extensionClasses, resourceURL, Class.forName(clazz, true, classLoader), name, overridden);
                }
                // 这里省略了其他部分代码
            }
    } catch (Throwable t) {
        logger.error("Exception occurred when loading extension class (interface: " +
            type + ", class file: " + resourceURL + ") in " + resourceURL, t);
    }
}
                  ↓
private void loadClass(Map<String, Class<?>> extensionClasses, java.net.URL resourceURL, Class<?> clazz, String name,
                       boolean overridden) throws NoSuchMethodException {
    if (!type.isAssignableFrom(clazz)) {
        throw new IllegalStateException("Error occurred when loading extension class (interface: " +
            type + ", class line: " + clazz.getName() + "), class "
            + clazz.getName() + " is not subtype of interface.");
    }
    // 如果该接口的实现类上有 Adaptive 注解的话，则给 cachedAdaptiveClass 字段进行了赋值
    if (clazz.isAnnotationPresent(Adaptive.class)) {
        cacheAdaptiveClass(clazz, overridden);
    } 
    // 如果该接口的实现类有个构造方法的参数是该接口的话，又怎么怎么滴
    else if (isWrapperClass(clazz)) {
        cacheWrapperClass(clazz);
    } else {
        // 省略其他部分代码
    }
}
                  ↓
// 如果 cachedAdaptiveClass 为空的话，就直接赋值
// 再次看到这个 cachedAdaptiveClass 字段时，之前在获取自适应扩展点不是也见过的么
private void cacheAdaptiveClass(Class<?> clazz, boolean overridden) {
    if (cachedAdaptiveClass == null || overridden) {
        cachedAdaptiveClass = clazz;
    } else if (!cachedAdaptiveClass.equals(clazz)) {
        throw new IllegalStateException("More than 1 adaptive class found: "
            + cachedAdaptiveClass.getName()
            + ", " + clazz.getName());
    }
}
```

##### 流程

- 首先，从当前系统及其引用的 Jar 包中，找到 SPI 接口的所有资源文件。
- 然后，循环每个资源文件读取文件内容，并逐行解析。
- 最后，在解析的过程中，通过 Class.forName 加载类路径得到类信息，并且针对类信息探测是否有 @Adaptive 注解，是否有入参就是 SPI 接口类型的构造方法。

#### @Adaptive 使用说明

1. @Adaptive 不仅会出现在 SPI 接口的方法上，也会出现在 SPI 接口的实现类上，因此自适应扩展点有 2 个来源，实现类、生成的代理类。
2. 获取自适应扩展点时，若实现类上有 @Adaptive 注解，则优先使用这个实现类作为自适应扩展点。验证源码推测

**想动态地指定 URL 中的参数，来动态切换实现类去执行业务逻辑，把一堆根据参数获取实现类的重复代码，全部封装到了代理类中，以达到充分灵活扩展的效果。**

#### 使用缺点

第一，占用内存。生成代理类必然会占据内存空间，如果系统中有大量的业务类都去生成自定义的代理类，就需要权衡生成代理类的合理性了。
第二，频繁改动 SPI 文件内容。如果某个接口经常新增实现类，不但需要经常修改 SPI 文件的内容，还得重新发布应用上线，才能拥有新增的实现类功能。
第三，对开发人员的开发门槛和素质要求较高。既然往自定义代理这方面靠，业务功能就要足够抽象，避免将来随着业务逻辑的新增，实现类的扩展难以支撑未来的变化。

## 课程地址

[17｜Adaptive适配：Dubbo的Adaptive特殊在哪里？]([17｜Adaptive适配：Dubbo的Adaptive特殊在哪里？ (geekbang.org)](https://time.geekbang.org/column/article/620941))